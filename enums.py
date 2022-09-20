from enum import IntEnum
from enum import Enum


ETH_TYPE_INSYS = 0xABBA


# STATES
class SlacState(IntEnum) :
    STATE_UNMATCHED = 0
    STATE_MATCHING = 1
    STATE_MATCHED = 2
    STATE_UNMACHING = 3

class ProgramState(IntEnum) :
    INITIAL_SETUP = 1
    WORK = 2


class ModuleState (IntEnum) :
    PAIRE = 1
    UNPAIR = 2


class Timers(float, Enum):
    """
    Timeouts defined by ISO15118-3 in table A.1
    All times are in seconds
    """

    # Time between the moment the EVSE detects state B and the reception of the
    # first SLAC Message, i.e. CM_SLAC_PARM.REQ.
    # This Timer is actually set in the environment.py, for debugging and
    # development reasons, allowing a easier setting of the time with the
    # docker-compose.dev.yml
    SLAC_INIT_TIMEOUT = 50.0  # [TT_EVSE_SLAC_init=20 s - 50 s]

    # Timeout for the reception of either CM_VALIDATE.REQ or CM_SLAC_MATCH.REQ
    # message, after reception of CM_ATTEN_CHAR.RSP
    SLAC_MATCH_TIMEOUT = 10.0  # [TT_EVSE_match_session=10 s]

    # Time the EV shall wait for CM_ATTEN_CHAR.IND after sending the first
    # CM_START_ATTEN_CHAR.IND
    SLAC_ATTEN_RESULTS_TIMEOUT = 1.2  # [TT_EV_atten_results = 1200 ms]

    # Timeout used for awaiting for a Request
    SLAC_REQ_TIMEOUT = 0.4  # [TT_match_sequence = 400 ms]

    # Timeout used for awaiting for a Response
    SLAC_RESP_TIMEOUT = 0.2  # [TT_match_response = 200 ms]

    # According to the standard:
    # [V2G3-A09-124] - In case the matching process is considered as FAILED,
    # wait for a time of TT_ matching_rate before restarting the process.

    # [V2G3-A09-125] - If the matching process fails for all retries started
    # within TT_matching_repetition, the matching process shall be stopped
    # in “Unmatched” state (see Figure 11).

    # The number maximum of retries is defined by C_conn_max_match = min 3
    # So, if within the TT_matching_repetition (10 s) time, the number of
    # retries expires, the matching process shall be stopped
    # in “Unmatched” state. (ISO Requirement couldnt be found for this,
    # but this is the logical steps to do)

    # Total time while the new SLAC repetitions can happen.
    # Once this timer is expired, the Matching process is considered FAILED
    SLAC_TOTAL_REPETITIONS_TIMEOUT = 10.0  # [TT_matching_repetition = 10 s]

    # Time to wait for the repetition of the matching process
    SLAC_REPETITION_TIMEOUT = 0.4  # [TT_matching_rate = 400 ms]

    # Time required to await while in state E or F (used in some use cases,
    # like the one defined by [V2G3 M06-07])
    SLAC_E_F_TIMEOUT = 4.0  # [T_step_EF = min 4 s]


BUFF_MAX_SIZE = 1500




