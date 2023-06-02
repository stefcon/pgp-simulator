from lib.index import *


def main():
    message = 'Hello World!'

    # Intialize message
    msg = Msg()
    msg.data = message
    msg.enc = 'AES'
    msg.auth = 'RSA'
    msg.uze_zip = True
    msg.uze_rad64 = True

    # Initialize key ring
    rsa_key = RSA_Wrapper.generate_key(2048)
    public_key_ring.add_entry(0, rsa_key, 'adf@adfs.com', 'brr', 'RSA')
    private_key_ring.add_entry(0, rsa_key, 'adf@adfs.com', 'brr', 'aaa', 'RSA')


    pipeline = SendPipeline(msg, 'test.txt', 0, 0, 'brr')
    msg = pipeline.run()

    print(msg.data)

    # pipeline = ReceivePipeline('test.txt')


if  __name__ == '__main__':
    main()