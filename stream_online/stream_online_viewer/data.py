from random import random

import numpy
from matplotlib import pyplot


def get_stream_message_data(image, metadata):
    """
    Create stream data payload from provided image and metadata.
    :param image: Image to prepare the message data for.
    :param metadata: Metadata to add to the message.
    :return: Dictionary with stream message payload.
    """

    stream_data = {
        "image": image,
        "image_size_x": image.shape[1],
        "image_size_y": image.shape[0],
        "image_profile_x": image.sum(0),
        "image_profile_y": image.sum(1)
    }

    stream_data.update(metadata)

    return stream_data


def generate_image(size_x=640, size_y=480, beam_size_x=10, beam_size_y=8, noise=0.1):
    """
    Generate a 2D numpy array with a simulated beam image.
    :param size_x: Width of the generated image.
    :param size_y: Height of the generated image.
    :param beam_size_x: Width of the simulated beam in the image.
    :param beam_size_y: Height of the simulated beam in the image.
    :param noise: Noise level to introduce to the image.
    :return: Numpy array with the image.
    """

    beam_x = numpy.linspace(-beam_size_x + numpy.random.rand(),
                            beam_size_x + numpy.random.rand(),
                            size_y)

    beam_y = numpy.linspace(-beam_size_y + numpy.random.rand(),
                            beam_size_y + numpy.random.rand(),
                            size_x)

    x, y = numpy.meshgrid(beam_y, beam_x)

    image = numpy.exp(-(x ** 2 + y ** 2))

    image += numpy.random.random((size_y, size_x)) * noise

    return image


def generate_metadata(beam_energy_base=5, repetition_rate=100):
    """
    Generate metadata to be send over with every image.
    :return: Dictionary of metadata.
    """
    return {
        "beam_energy": beam_energy_base + ((beam_energy_base*0.1) * random()),
        "repetition_rate": repetition_rate
    }


def display_image(image):
    """
    Debug method to display image on screen.
    :param image: Image to display.
    """
    pyplot.imshow(image)
    pyplot.show()


def save_image(image):
	"""
	Save image to local disk
	"""	
	pyplot.imshow(image)
	pyplot.savefig("./static/pic.jpg")
