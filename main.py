import sys
import files_processor
import logger


def main():
    lgr = logger.Logger.__call__().get_logger()
    if sys.argv[1]:
        lgr.info("Trying to process {} \
        dir...".format(sys.argv[1]))
        files_processor.decompress_unpack_files(sys.argv[1])
    elif not sys.argv[1]:
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


if __name__ == "__main__":
    main()
