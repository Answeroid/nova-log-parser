import os
import bz2
import gzip
import shutil
import logger


lgr = logger.Logger.__call__().get_logger()


def _collect_files(walk_dir="./"):
    """
    Collect list of absolute file paths of given dir

    :param walk_dir: {[str]} -- path to directory
    to use it as root and traverse over subdirs
    and get all absolute file paths as a list
    :return: {[list]} list with files paths
    """

    lgr.info("Collecting files from {} dir".format(os.path.abspath(walk_dir)))
    files_paths_list = []
    for root, _, files in os.walk(os.path.abspath(walk_dir)):
        for filename in files:
            file_path = os.path.join(root, filename)
            files_paths_list.append(file_path)
        lgr.debug("files_paths_list:\n{}", format(files_paths_list))
        lgr.info("Processed given dir...")
    return files_paths_list


def _bz2_unpacker(files_paths_list):
    """
    Takes a list with absolute file paths
    and decompress them 1 by 1 from .bz2
    to original file to the same dir

    :param files_paths_list: {[list]} -- list with absolute file paths
    :return:
    """

    lgr.info("Searching for .bz2 files...")

    for file_path in files_paths_list:
        lgr.debug("Processing file {}...".format(file_path))
        if file_path.endswith('.bz2'):
            new_file_path = file_path.replace('.bz2', '')
            lgr.debug("File {} compressed, trying to decompress "
                      "it to {} ...".format(file_path, new_file_path))
            with open(new_file_path, 'wb') as new_file, bz2.BZ2File(file_path, 'rb') as file:
                for data in iter(lambda: file.read(100 * 1024), b''):
                    lgr.debug("Writing data to {} ...".format(new_file_path))
                    new_file.write(data)
                    lgr.debug("Decompressed successfully!")


def _gz_unpacker(files_paths_list):
    """
    Takes a list with absolute file paths
    and unzip them 1 by 1 from .gz
    to original file to the same dir

    :param files_paths_list: {[list]} -- list with absolute file paths
    :return: None
    """

    for file_path in files_paths_list:
        lgr.debug("Processing file {}...".format(file_path))
        if file_path.endswith('.gz'):
            new_file_path = file_path.replace('.gz', '')
            lgr.debug("File {} compressed, trying to decompress "
                      "it to {} ...".format(file_path, new_file_path))
            with gzip.open(file_path, 'rb') as file_in:
                with open(new_file_path, 'wb') as file_out:
                    lgr.debug("Copying file object "
                              "from {} to {} ...".format(file_path, new_file_path))
                    shutil.copyfileobj(file_in, file_out)
            lgr.debug("Unpacked successfully!")


def decompress_unpack_files(walk_dir):
    """
    Decompress and unpack files from given folder

    :param walk_dir: {[str]} -- path to logs directory
    :return: None
    """

    _bz2_unpacker(_collect_files(walk_dir))
    _gz_unpacker(_collect_files(walk_dir))


def collect_logs(walk_dir="./"):
    """
    Collects not compressed/archived log files
    :param walk_dir: {[str]} -- path to logs directory
    :return: {[list]} -- list with not compressed/archived log files
    """

    lgr.info("Collecting files from {} dir...".format(walk_dir))
    files_paths_list = _collect_files(walk_dir)
    ready_log_files = []
    for file_path in files_paths_list:
        if not file_path.endswith(".bz2") and not file_path.endswith(".gz"):
            lgr.debug("Found {} file which seems to be ready "
                      "for processing...Collected.".format(file_path))
            ready_log_files.append(file_path)
    lgr.debug("ready_log_files:\n{}".format(ready_log_files))
    lgr.info("Processed given dir...")
    return ready_log_files
