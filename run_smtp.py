import asyncio
from aiosmtpd.controller import Controller

class DebugHandler:
    async def handle_DATA(self, server, session, envelope):
        print('---------- INCOMING EMAIL ----------')
        print(f'From: {envelope.mail_from}')
        print(f'To: {envelope.rcpt_tos}')
        print('Message data:')
        print(envelope.content.decode('utf8', errors='replace'))
        print('------------------------------------')
        return '250 Message accepted for delivery'

if __name__ == '__main__':
    controller = Controller(DebugHandler(), hostname='localhost', port=1025)
    controller.start()
    print("Debug SMTP server running on localhost:1025...")
    try:
        asyncio.get_event_loop().run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        controller.stop()
