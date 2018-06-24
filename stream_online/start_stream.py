import argparse

from stream_online_viewer.stream import generate_stream


def main():
    parser = argparse.ArgumentParser(description='Camera stream simulator')
    parser.add_argument('-o', '--output_port', default=8888, type=int, help="Stream output port.")
    parser.add_argument('-n', '--n_images', default=-1, type=int, help="Number of images to generate in the stream "
                                                                       "(-1 == infinite).")
    parser.add_argument('-d', '--delay', default=0.1, type=float, help="Delay between each message on the stream.")

    arguments = parser.parse_args()

    print("Generating stream on port %d with n_images %d and delay %f." % (arguments.output_port,
                                                                          arguments.n_images,
                                                                          arguments.delay))

    generate_stream(output_port=arguments.output_port,
                    n_images=arguments.n_images,
                    delay=arguments.delay)


if __name__ == "__main__":
    main()
