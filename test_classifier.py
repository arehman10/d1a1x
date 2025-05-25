import csv
import os
from isic_classifier import classify_file


def test_classify_file(tmp_path):
    input_csv = os.path.join(tmp_path, 'input.csv')
    output_csv = os.path.join(tmp_path, 'output.csv')
    # copy sample activities file
    with open('sample_activities.csv', 'r', encoding='utf-8') as src:
        data = src.read()
    with open(input_csv, 'w', encoding='utf-8') as dst:
        dst.write(data)

    classify_file(input_csv, output_csv)

    with open(output_csv, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        results = list(reader)

    codes = [row['isic_code'] for row in results]
    assert codes[0] == '0112'
    assert codes[1] == '6201'
    assert codes[2] == '5610'
    assert codes[3] == '5510'
    assert codes[4] == '9311'
