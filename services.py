"""The module for services."""
import json
import logging
import os
import re
from datetime import datetime

import sqlalchemy as db
from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from models import Log, Report

load_dotenv()

MYSQL_DATABASE_URL = os.getenv('MYSQL_DATABASE_URL')
LOG_FILENAME = os.getenv('LOG_FILENAME')

engine = create_engine(MYSQL_DATABASE_URL)

logging.basicConfig(
    filename='app.log',
    filemode='w',
    format='%(name)s - %(levelname)s - %(message)s'
)


def split(input_str):
    """Splits the input string by one or more spaces."""
    return re.split(r'\s{1,}', input_str)


def calc_max_report_number(session):
    """Calculates the max number of report."""
    report = session.query(db.func.max(Report.report_number)).one()
    if report[0]:
        return report[0]
    return 0


def read_from_directory(dirname):
    """Reads files from directory."""
    dirname = dirname.strip()
    if os.path.exists(dirname) and os.path.isdir(dirname):
        return os.listdir()
    return []


def write_json(filename, data):
    """Writes JSON to the output file."""
    filename = filename.strip()
    with open(filename, "w") as fp:
        json.dump(data, fp)


def read_and_save_to_db(filenames):
    """Reads the input files."""
    if len(filenames) == 0:
        return
    with Session(engine) as session:
        max_report_number = calc_max_report_number(session)
        max_report_number += 1
        report = Report(
            report_number=max_report_number,
        )
        session.add(report)
        for filename in filenames:
            filename = filename.strip()
            print(f"Reading the input file {filename}")
            try:
                with open(filename) as fp:
                    for i, line in enumerate(fp):
                        line = line.rstrip()
                        str_values = split(line)
                        if len(str_values) < 6:
                            idx = i + 1
                            logging.error(
                                f"Incorrect line {idx} in the file {filename}"
                            )
                            continue
                        timestamp = datetime.fromtimestamp(
                            float(str_values[0])
                        )
                        log = Log(
                            timestamp=timestamp,
                            response_header_size=str_values[1],
                            ip_address=str_values[2],
                            response_code=str_values[3],
                            response_size=str_values[4],
                            request_method=str_values[5],
                            report=report,
                        )
                session.add(log)
            except IOError:
                logging.error(f"Could not read the file {filename}")
            else:
                print(f"End of file reading {filename}")
        session.commit()


def calc_most_frequent_ip():
    """Calculates the most frequent IP."""
    sql = """
        SELECT l.ip_address, COUNT(*) count_ip
        FROM logs l
        WHERE l.report_id IN (
            SELECT r.id
            FROM reports AS r
            WHERE r.report_number = (
                SELECT MAX(rep.report_number)
                FROM reports AS rep
            )
        )
        GROUP BY l.ip_address
        ORDER BY count_ip DESC
    """

    with Session(engine) as session:
        records = session.execute(sql)

    ips = [record[0] for record in records]
    if ips and ips[0]:
        ip_address = ips[0]
    else:
        ip_address = ""

    return {"most-frequent-ip": ip_address}


def calc_less_frequent_ip():
    """Calculates the less frequent IP."""
    sql = """
        SELECT l.ip_address, COUNT(*) count_ip
        FROM logs l
        WHERE l.report_id IN (
            SELECT r.id
            FROM reports AS r
            WHERE r.report_number = (
                SELECT MAX(rep.report_number)
                FROM reports AS rep
            )
        )
        GROUP BY l.ip_address
        ORDER BY count_ip
    """

    with Session(engine) as session:
        records = session.execute(sql)

    ips = [record[0] for record in records]
    if ips and ips[0]:
        ip_address = ips[0]
    else:
        ip_address = ""

    return {"less-frequent-ip": ip_address}


def calc_events_per_second():
    """Calculate the number of elements per hour."""
    sql = """
        SELECT COUNT(*) count_event
        FROM logs l
        WHERE l.report_id IN (
            SELECT r.id
            FROM reports AS r
            WHERE r.report_number = (
                SELECT MAX(rep.report_number)
                FROM reports AS rep
            )
        )
        GROUP BY SECOND(l.timestamp)
    """

    with Session(engine) as session:
        records = session.execute(sql)

    events = [record[0] for record in records]

    events_list = []
    for event in events:
        event_dict = {"event-number": event}
        events_list.append(event_dict)

    return events_list


def calc_size_total_amount():
    """Calculates the total amount of bytes exchanged."""
    sql = """
        SELECT SUM(l.response_header_size + l.response_size) total_size
        FROM logs l
        WHERE l.report_id IN (
            SELECT r.id
            FROM reports AS r
            WHERE r.report_number = (
                SELECT MAX(rep.report_number)
                FROM reports AS rep
            )
        )
    """

    with Session(engine) as session:
        records = session.execute(sql)

    total_sizes = [record[0] for record in records]
    if total_sizes and total_sizes[0]:
        total_size = str(total_sizes[0])
    else:
        total_size = ""

    return {"total-amount-exchanged": total_size}
