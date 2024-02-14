import exiftool
import os
import re


def metadata_title_from_mp4(video_file):
    # Converts title.mp4 to metadata/title.dat
    return "metadata/" + video_file.split(".")[0] + ".dat"


def write_metadata_to_file(video_file, metadata_file):
    
    et = exiftool.ExifToolHelper()

    # "-api largefilesupport=1" allows to read large files
    # "-a" allows to read all metadata
    # "-b" returns binary data
    # "-ee" returns extended embedded metadata 
    metadata = et.execute("-api", "largefilesupport=1", "-a", "-ee", video_file)
    
    with open(metadata_file, "w") as f:
        f.write(metadata)
    
    print(f"Metadata from {video_file} written to {metadata_file}")


def read_metadata_from_video(video_file):

    metadata_file = metadata_title_from_mp4(video_file)

    # If file doesn't exist, write to file
    if not os.path.exists(metadata_file):
        print(f"Couldn't find metadata for {video_file}, writing to {metadata_file}")
        write_metadata_to_file(video_file, metadata_file)
    else:
        print(f"Found metadata file for {video_file}")
    
    # Read file
    with open(metadata_file, "r") as f:
        metadata = f.read()
    
    # If file exists but is empty, write to file
    if len(metadata) == 0:
        print(f"File {metadata_file} is empty, writing metadata")
        write_metadata_to_file(video_file, metadata_file)
    
    # Read file
    with open(metadata_file, "r") as f:
        metadata = f.read()

    # Return content as list of lines
    return metadata.split("\n")


def filter_metadata_line(category, title, line) -> str | None:
    # TODO: Error handling

    # [Category] Title : Data
    s = re.search(r"\[{}\] +{} +: (.*)".format(category, title), line)
    return s if s is None else s.group(1)


def parse_metadata(metadata):
    video_config = {}
    gps_data = {
        "latitude": [],
        "longitude": [],
        "altitude": [],
        "speed": []
    }

    for line in metadata:
        # Video Title
        if "title" not in video_config:
            title = filter_metadata_line("File", "File Name", line)
            if not title is None:
                video_config["title"] = title
                continue
        # Video Duration
        if "duration" not in video_config:
            duration = filter_metadata_line("QuickTime", "Duration", line)
            if not duration is None:
                video_config["duration"] = float(duration)
                continue
        # Video Frame Rate
        if "fps" not in video_config:
            fps = filter_metadata_line("QuickTime", "Video Frame Rate", line)
            if not fps is None:
                video_config["fps"] = int(fps)
                continue
        
        # GPS Latitude
        gps_lat = filter_metadata_line("GoPro", "GPS Latitude", line)
        if not gps_lat is None:
            gps_data["latitude"].append(float(gps_lat))
            continue
        # GPS Longitude
        gps_lng = filter_metadata_line("GoPro", "GPS Longitude", line)
        if not gps_lng is None:
            gps_data["longitude"].append(float(gps_lng))
            continue
        # GPS Altitude    
        gps_alt = filter_metadata_line("GoPro", "GPS Altitude", line)
        if not gps_alt is None:
            gps_data["altitude"].append(float(gps_alt))
            continue
        # GPS Speed
        gps_spd = filter_metadata_line("GoPro", "GPS Speed", line)
        if not gps_spd is None:
            gps_data["speed"].append(float(gps_spd))
            continue

    return {
        "video_config": video_config,
        "gps_data": gps_data
    }
