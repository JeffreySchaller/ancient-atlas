#!/usr/bin/env python3
"""Validate map data, uncertain origins, and locally served licensed photographs."""
import json
import math
import re
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / 'public'
records = json.loads((PUBLIC / 'data/obelisks.json').read_text())
assert records == json.loads((ROOT / 'data/obelisks.json').read_text()), 'Public collection must match the editorial source.'
categories = {'pharaonic','ptolemaic','egyptian_undated','roman','disputed','unfinished','replica'}
ids = set()
photos = 0
stops = 0
videos = 0

def point(lat, lon, nullable=False):
    if nullable and lat is None and lon is None:
        return
    assert isinstance(lat,(int,float)) and math.isfinite(lat) and -90 <= lat <= 90
    assert isinstance(lon,(int,float)) and math.isfinite(lon) and -180 <= lon <= 180

def link(url):
    parsed = urlparse(url)
    assert parsed.scheme == 'https' and parsed.netloc, url

assert isinstance(records,list) and records, 'The collection must contain monument records.'
for record in records:
    key = record['id']
    assert key not in ids, f'Duplicate monument: {key}'
    ids.add(key)
    for field in ['name','city','country','material','summary','original_site','origin_label','origin_note','checked_date']:
        assert isinstance(record[field],str) and record[field].strip(), (key,field)
    assert record['category'] in categories, key
    point(record['lat'],record['lon'])
    point(record['origin_lat'],record['origin_lon'],nullable=True)
    assert record['shaft_height_m'] is None or record['shaft_height_m'] > 0, key
    assert record['mass_t'] is None or isinstance(record['mass_t'],(int,float)), key
    assert record['sources'], key
    for source in record['sources']:
        assert source['title'].strip()
        link(source['url'])
    journey = record['journey']
    assert journey, key
    for stop in journey:
        for field in ['date','place','note','coordinate_note']:
            assert isinstance(stop[field],str) and stop[field].strip(), (key,field)
        point(stop['lat'],stop['lon'],nullable=True)
        stops += 1
    endpoint = journey[-1]
    assert endpoint['lat'] is not None and abs(endpoint['lat']-record['lat']) < .02, key
    assert endpoint['lon'] is not None and abs(endpoint['lon']-record['lon']) < .02, key
    assert record['photos'], f'No photograph for {key}'
    for photo in record['photos']:
        for field in ['creator','license','title','alt','changes']:
            assert isinstance(photo[field],str) and photo[field].strip(), (key,field)
        link(photo['source_url']); link(photo['license_url'])
        assert photo['src'].startswith('/assets/obelisks/'), key
        path = (PUBLIC / photo['src'].lstrip('/')).resolve()
        assert path.is_relative_to((PUBLIC/'assets/obelisks').resolve())
        assert path.is_file() and path.stat().st_size > 1000, path
        assert path.read_bytes()[:3] == b'\xff\xd8\xff', f'Expected JPEG: {path}'
        assert photo['width'] > 0 and photo['height'] > 0, key
        photos += 1
    if record['category'] == 'replica':
        assert record['origin_lat'] is None and record['origin_lon'] is None
        assert record.get('model_location'), key
    if 'archival_photo' in record:
        assert record['archival_photo']['title'].strip(), key
        link(record['archival_photo']['url'])
    video_ids = set()
    for video in record.get('videos', []):
        assert re.fullmatch(r'[A-Za-z0-9_-]{11}', video['id']), (key, video['id'])
        assert video['id'] not in video_ids, (key, video['id'])
        video_ids.add(video['id'])
        for field in ['title', 'label', 'creator', 'description']:
            assert isinstance(video[field], str) and video[field].strip(), (key, field)
        start = video.get('start', 0)
        assert type(start) is int and start >= 0, key
        if 'source_url' in video:
            link(video['source_url'])
        videos += 1
    if record['category'] == 'unfinished':
        assert record['shaft_height_m'] is None, 'An unfinished quarry stone is not a standing shaft.'
        assert record.get('planned_length_m'), key

assert len(ids) == len(records)
print(f'Validated {len(records)} monuments, {stops} journey milestones, {photos} credited photographs and {videos} video links.')
