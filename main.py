import sys
import files_processor
import logger


def main():
    lgr = logger.Logger.__call__().get_logger()

    if 1 < len(sys.argv):
        lgr.info("Trying to process {} \
        dir...".format(sys.argv[1]))
        files_processor.decompress_unpack_files(sys.argv[1])
    elif len(sys.argv) < 2:
        try:
            lgr.info("Did not find cmd argument, \
            processing default logs dir...")
            files_processor.decompress_unpack_files("logs")
        except EnvironmentError:
            lgr.info("Did not find default logs dir...")
            lgr.debug("Did not find default \
            logs dir...", exc_info=True)
    else:
        raise EnvironmentError("Unknown error occurred or \
        log directory was not provided...")

    lgr.info("Getting file objects...")
    file_objects = files_processor.get_file_objects(sys.argv[1])
    lgr.info("Processing log lines...")

    parsed_log_entries = []
    for file_object in file_objects:
        for entry in file_object:
            parsed_log_entries.append(files_processor.parse_log_entry(entry))

    log_entries_objects = []
    for parsed_log_entry in parsed_log_entries:
        log_entries_objects.append(files_processor.create_parsed_log_entry_object(parsed_log_entry))

    lgr.debug("BINGO!!!")
    import pdb
    pdb.set_trace()


if __name__ == "__main__":
    main()
