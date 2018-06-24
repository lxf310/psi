from time import sleep

from bsread.sender import sender

from stream_online_viewer import data


def generate_and_send_message(output_stream):
    """
    Generate a test message and send it out.
    :param output_stream: Stream to send the message on.
    """
    image = data.generate_image()
    metadata = data.generate_metadata()

    data_to_send = data.get_stream_message_data(image, metadata)

    output_stream.send(data=data_to_send)


def generate_stream(output_port=8888, n_images=1000, delay=0.1):
    """
    Open a stream and generate the simulated messages. This call is blocking.
    :param output_port: Port to bind the output stream to.
    :param n_images: Number of images to send (-1 == infinite)
    :param delay: How much time in seconds to wait between each message. 0.1 == 10Hz.
    """

    with sender(port=output_port) as output_stream:

        if n_images == -1:
            while True:
                generate_and_send_message(output_stream)
                sleep(delay)

        else:
            for _ in range(n_images):
                generate_and_send_message(output_stream)
                sleep(delay)
