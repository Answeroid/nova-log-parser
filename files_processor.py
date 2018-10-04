import os
import re
import bz2
import gzip
import shutil
from LogEntry import LogEntry
import logger

import pdb


lgr = logger.Logger.__call__().get_logger()


def _collect_files(walk_dir="./"):
    """
    Collect list of absolute file paths of given dir

    :param walk_dir: {[str]} -- path to directory
    to use it as root and traverse over subdirs
    and get all absolute file paths as a list
    :return: list[str]
    """

    lgr.info("Collecting files from {} dir".format(os.path.abspath(walk_dir)))
    files_paths_list = []
    for root, _, files in os.walk(os.path.abspath(walk_dir)):
        for filename in files:
            file_path = os.path.join(root, filename)
            files_paths_list.append(file_path)
        lgr.debug("files_paths_list:\n{}".format(files_paths_list))
        lgr.info("Processed {} dir...".format(os.path.abspath(walk_dir)))
    return files_paths_list


def _bz2_unpacker(files_paths_list):
    """
    Takes a list with absolute file paths
    and decompress them 1 by 1 from .bz2
    to original file to the same dir

    :param files_paths_list: list -- list with absolute file paths
    :return: None
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

    :param files_paths_list: list -- list with absolute file paths
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

    :param walk_dir: str -- path to logs directory
    :return: None
    """

    _bz2_unpacker(_collect_files(walk_dir))
    _gz_unpacker(_collect_files(walk_dir))


def collect_logs(walk_dir="./"):
    """
    Collects not compressed/archived log files
    :param walk_dir: str -- path to logs directory
    :return: list[str] -- list with not compressed/archived log files
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
    lgr.info("Processed {} dir...".format(os.path.abspath(walk_dir)))
    return ready_log_files


def get_file_objects(walk_dir="./"):
    """
    Get file objects
    :param walk_dir: str -- path to logs directory
    :return: list[Object]
    """

    lgr.info("Trying to get file objects...")
    file_objects = []
    ready_log_files = collect_logs(walk_dir)
    for log_file in ready_log_files:
        lgr.debug("Appending file {} to file_objects list...".format(log_file))
        file_objects.append(open(log_file, 'r'))
    lgr.debug("file_objects:\n{}".format(file_objects))
    return file_objects


def parse_log_entry(log_entry):
    """
    Parses raw log entry string
    and tries to create list
    with log entry artifacts

    :param log_entry: str --- raw log entry
    :return: list[str]
    """

    lgr.debug("Trying to parse raw log entry {} ...".format(log_entry))
    try:
        splitted_entry = log_entry.split(maxsplit=5)
        parsed_log_entry = splitted_entry[:5]

        requests = "-"
        users = "-"
        instance = "-"
        message = "-"

        if not splitted_entry == parsed_log_entry:
            leftover = splitted_entry[5]
            if not re.search("^\[(.*?)\]", leftover):
                message = leftover
            else:
                requests_and_users = re.search("\[(.*?)\]", leftover).group(1)
                instance_and_message = leftover.split("] ", 1)[1]
                if requests_and_users == "-":
                    pass
                else:
                    requests, users = requests_and_users.split(sep=" - ", maxsplit=1)
                instance, message = instance_and_message.split(maxsplit=1)
                if not re.match("^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$", instance):
                    instance = "-"
                    message = instance_and_message

        parsed_log_entry.append(requests)
        parsed_log_entry.append(users)
        parsed_log_entry.append(instance)
        parsed_log_entry.append(message)
        return parsed_log_entry

    except Exception as e:
        lgr.debug(e)
        lgr.debug(log_entry)
        pdb.set_trace()


def create_parsed_log_entry_object(parsed_log_entry):
    """
    Creates object from parsed log entry

    :param parsed_log_entry: list --- list with log entry artifacts.
    len(parsed_log_entry) == 9
    :return: LogEntry object
    """

    lgr.debug("Trying to create parsed log entry object from {} ...".format(parsed_log_entry))
    if len(parsed_log_entry) == 9:
        lgr.debug("Creating log entry object from ")
        asctime = parsed_log_entry[0]
        msecs = parsed_log_entry[1]
        process = parsed_log_entry[2]
        levelname = parsed_log_entry[3]
        name = parsed_log_entry[4]
        request_ids = parsed_log_entry[5]
        user_identitys = parsed_log_entry[6]
        instance = parsed_log_entry[7]
        message = parsed_log_entry[8]
        log_entry_object = LogEntry(asctime,
                                    msecs,
                                    process,
                                    levelname,
                                    name,
                                    request_ids,
                                    user_identitys,
                                    instance,
                                    message)
        return log_entry_object
    else:
        lgr.debug("Log entry {} does not match \
        a requirement, skipped...".format(parsed_log_entry))
