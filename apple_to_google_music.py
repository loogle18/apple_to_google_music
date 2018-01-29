from argparse import ArgumentParser
from gmusicapi import Mobileclient
from multiprocessing import Pool, cpu_count
from time import sleep


class bcolors:
    OKBLUE = "\033[94m"
    OKGREEN = "\033[92m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"


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


def _search_tracks(line, tried=False):
    columns = line.split("\t")
    query = "%s %s %s" % (columns[0], columns[1], columns[3])

    try:
        track_id = api.search(query)["song_hits"][0]["track"]["storeId"]
        print(bcolors.OKGREEN + query + bcolors.ENDC)
        return track_id
    except Exception:
        if not tried:
            sleep(3)
            _search_tracks(line, True)
        else:
            print(bcolors.FAIL + query + bcolors.ENDC)
            ignored_tracks.append(query)


def _print_message():
    print("\n--------------------------------------------------------\n\n")
    print(bcolors.OKGREEN + "Successfully connected to your account." +
          bcolors.ENDC)
    print("\n\nBelow you will see track full names in different colors. " +
          "Here's explanations:")
    print(bcolors.OKGREEN + "Track was found on Google Music " +
          "and will be added to your library." + bcolors.ENDC)
    print(bcolors.FAIL + "Track was not found on Google Music " +
          "and will be added to 'ignored_tracks.txt' file" + bcolors.ENDC)
    print("\n\n--------------------------------------------------------\n")
    print("\n\Starting process...\n\n\n")


def main():
    args = _get_args()
    am_songs_count = _get_songs_count_from_file(args.file)
    if am_songs_count:
        print(bcolors.OKBLUE +
              "Found %d songs in passed file" % am_songs_count + bcolors.ENDC)
        global api, ignored_tracks
        api = Mobileclient()
        ignored_tracks = []
        if api.login(args.email, args.password, Mobileclient.FROM_MAC_ADDRESS):
            _print_message()
            gm_track_ids = []
            with open(args.file) as file:
                pool = Pool(processes=cpu_count() + 1)
                lines = file.readlines()[1:]
                gm_track_ids = pool.map(_search_tracks, lines)
                pool.close()
                pool.join()

                gm_track_ids = [i for i in gm_track_ids if i is not None]

                if ignored_tracks:
                    with open("ignored_tracks.txt", "w") as ignored_list:
                        ignored_list.write("\n".join(ignored_tracks))


        else:
            print(bcolors.FAIL + "Could not connect to your account. " +
                  "Please check credentials." + bcolors.ENDC)

if __name__ == "__main__":
    main()
