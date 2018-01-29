from argparse import ArgumentParser
from gmusicapi import Mobileclient


def _get_args():
    parser = ArgumentParser()
    required = parser.add_argument_group("required arguments")
    required.add_argument("-e", "--email", metavar="\b", required=True,
                          help="Google Play Music email.")
    required.add_argument("-p", "--password", metavar="\b", required=True,
                          help="Generated app password. See: https://support.google.com/mail/answer/185833?hl=en")
    required.add_argument("-f", "--file", metavar="\b", required=True,
                          help="Path to Apple Music playlist file in txt format.")
    return parser.parse_args()


def _get_songs_count_from_file(path):
    try:
        with open(path) as file:
            return sum(1 for line in file) - 1
    except Exception as error:
        print(error)

def main():
    args = _get_args()
    am_songs_count = _get_songs_count_from_file(args.file)
    if am_songs_count:
        print("Found %d songs in passed file" % am_songs_count)
        api = Mobileclient()
        if api.login(args.email, args.password, Mobileclient.FROM_MAC_ADDRESS):
            print("Successfully connected to your account.")
        else:
            print("Could not connect to your account. Please check credentials.")

if __name__ == "__main__":
    main()
