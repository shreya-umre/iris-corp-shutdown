import sys
import os

# Add src to path so tests can import parser functions
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from parser import parse_date, classify_event, process_notices

def test_parse_date_valid():
    assert parse_date("2025-03-14") == "2025-03-14"
    assert parse_date("14.03.2025") == "2025-03-14"
    assert parse_date("14. März 2025") == "2025-03-14"

def test_classify_event_revocation():
    # Test confirmed closure classification
    legal = "§ 21 BImSchG"
    subject = "Vollständiger Widerruf der Genehmigung"
    assert classify_event(legal, subject) == "CONFIRMED_CLOSURE"

def test_classify_event_potential():
    # Test potential shutdown intent classification
    legal = "§ 15 BImSchG"
    subject = "Anzeige der beabsichtigten Stilllegung"
    assert classify_event(legal, subject) == "POTENTIAL_SHUTDOWN"

def test_classify_event_negative_control():
    # Test negative control (routine approval / water law)
    legal = "§ 16 BImSchG"
    subject = "Änderungsgenehmigung zur Errichtung einer Filteranlage"
    assert classify_event(legal, subject) == "NEGATIVE_CONTROL"

def test_pipeline_execution():
    records, errors = process_notices()
    # Verify that records were processed and bad records were caught
    assert len(records) > 0
    assert len(errors) == 2  # Updating to reflect the 2 actively caught exception cases