#!/usr/bin/env python3
import asyncio
import websockets
import json
import argparse
import traceback
from datetime import datetime, timezone


def mask_key(key: str) -> str:
    if not key or len(key) < 10:
        return '***masked***'
    return key[:4] + '*' * (len(key) - 8) + key[-4:]


async def connect_ais_stream(api_key, bounding_boxes, filters_mmsi, filter_message_types, count_target, pretty, debug=False, timeout=60, global_sample=False):
    uri = "wss://stream.aisstream.io/v0/stream"

    # Se richiesto, prima prova connettività con un sample globale
    if global_sample and filters_mmsi:
        print("=== TEST CONNETTIVITÀ: sample dal feed globale ===")
        global_sub = {
            "APIKey": api_key,
            "BoundingBoxes": bounding_boxes,
            "FilterMessageTypes": filter_message_types,
        }

        try:
            async with websockets.connect(uri) as websocket:
                await websocket.send(json.dumps(global_sub))
                print("Feed globale connesso, attendendo 1 messaggio per test...")
                message_json = await asyncio.wait_for(websocket.recv(), timeout=10)
                message = json.loads(message_json)
                if message.get('MessageType') == 'PositionReport':
                    meta = message.get('MetaData', {})
                    print(f"✓ Test OK: ricevuto PositionReport da MMSI {meta.get('MMSI')} ({meta.get('ShipName')})")
                else:
                    print(f"✓ Test OK: ricevuto messaggio {message.get('MessageType')}")
        except asyncio.TimeoutError:
            print("✗ WARNING: Timeout nel feed globale - problema di connettività?")
        except Exception as e:
            print(f"✗ ERROR nel test globale: {e}")

        print("=== INIZIO RICERCA MMSI SPECIFICO ===")

    subscribe_message = {
        "APIKey": api_key,
        "BoundingBoxes": bounding_boxes,
        "FilterMessageTypes": filter_message_types,
    }

    # solo se abbiamo MMSI specifici aggiungiamo il filtro
    if filters_mmsi:
        subscribe_message["FiltersShipMMSI"] = filters_mmsi

    if debug:
        # stampiamo il payload di subscribe, ma mascheriamo la chiave
        s = dict(subscribe_message)
        s["APIKey"] = mask_key(s.get("APIKey"))
        print("[DEBUG] Subscribe payload:", json.dumps(s))

    try:
        async with websockets.connect(uri) as websocket:
            print("connesso")
            await websocket.send(json.dumps(subscribe_message))
            if filters_mmsi:
                print(f"subscription inviata per MMSI: {', '.join(filters_mmsi)}")
                print(f"Attendendo fino a {timeout}s per messaggi da queste navi...")
            else:
                print("subscription inviata per feed globale")

            # se siamo in debug proviamo a leggere il primo messaggio con timeout
            if debug:
                try:
                    first = await asyncio.wait_for(websocket.recv(), timeout=5)
                    print("[DEBUG] Primo messaggio ricevuto:", first[:200] + "..." if len(first) > 200 else first)
                except asyncio.TimeoutError:
                    print("[DEBUG] Timeout: nessun messaggio ricevuto nei primi 5s dopo subscribe")

            count = 0
            start_time = asyncio.get_event_loop().time()

            async for message_json in websocket:
                # Check timeout per MMSI specifici
                if filters_mmsi and (asyncio.get_event_loop().time() - start_time) > timeout:
                    print(f"⏰ TIMEOUT: {timeout}s trascorsi senza messaggi per MMSI {', '.join(filters_mmsi)}")
                    print("   Le navi potrebbero essere spente, ancorate, o fuori copertura.")
                    print("   Prova con --global-sample per testare la connettività.")
                    print("\n💡 SUGGERIMENTO: Prova questi comandi:")
                    print(f"   python3 get_info.py --pretty -n 5    # Vedi 5 navi attive ora")
                    print(f"   python3 get_info.py {' '.join(filters_mmsi)} --timeout 300 --pretty  # Attendi 5 minuti")
                    break
            async for message_json in websocket:
                try:
                    message = json.loads(message_json)
                except Exception:
                    print("Messaggio non JSON ricevuto:", message_json)
                    continue

                if 'error' in message:
                    print("ERRORE dal server:", message.get('error'))
                    continue

                message_type = message.get('MessageType')
                if message_type == 'PositionReport':
                    ais_message = message['Message'].get('PositionReport', {})
                    meta = message.get('MetaData', {})
                    mmsi = meta.get('MMSI') or ais_message.get('UserID')

                    # filtro lato client: confrontiamo come stringhe
                    if filters_mmsi and str(mmsi) not in [str(x) for x in filters_mmsi]:
                        continue

                    if pretty:
                        ts = meta.get('time_utc') or datetime.now(timezone.utc).isoformat()
                        print(f"[{ts}] MMSI:{ais_message.get('UserID')} Ship:{meta.get('ShipName')} lat:{ais_message.get('Latitude')} lon:{ais_message.get('Longitude')} sog:{ais_message.get('Sog')} cog:{ais_message.get('Cog')}")
                    else:
                        print(message_json)

                    count += 1
                    if count >= count_target:
                        print(f"--- FINE: ricevuti {count_target} messaggi ---")
                        break

    except Exception as e:
        print("Connessione fallita o errore inaspettato:", str(e))
        if debug:
            traceback.print_exc()


def build_args():
    parser = argparse.ArgumentParser(description='AISStream MMSI query')
    parser.add_argument('mmsi', nargs='*', help='One or more MMSI to query (optional - if omitted, receives global feed)')
    parser.add_argument('-n', '--count', type=int, default=10, help='Number of matching messages to receive before exit')
    parser.add_argument('--pretty', action='store_true', help='Pretty print selected fields')
    parser.add_argument('--apikey', default=None, help='API key (overrides hardcoded)')
    parser.add_argument('--debug', action='store_true', help='Enable debug prints (masked payload + first-message timeout)')
    parser.add_argument('--timeout', type=int, default=60, help='Timeout in seconds for specific MMSI search (default: 60)')
    parser.add_argument('--global-sample', action='store_true', help='Show sample from global feed first to check connectivity')
    return parser


def main():
    parser = build_args()
    args = parser.parse_args()

    api_key = args.apikey or '82321a1c2ee896aedff9ccaf22389d380382fae7'
    bounding_boxes = [[[-90, -180], [90, 180]]]
    filters_mmsi = args.mmsi if args.mmsi else None  # None = global feed
    filter_message_types = ['PositionReport']
    count_target = args.count
    pretty = args.pretty
    debug = args.debug
    timeout = args.timeout
    global_sample = args.global_sample

    asyncio.run(connect_ais_stream(api_key, bounding_boxes, filters_mmsi, filter_message_types, count_target, pretty, debug, timeout, global_sample))


if __name__ == '__main__':
    main()
