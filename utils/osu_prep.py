from . import tools
import numpy as np

# Decodes a osu file into a object


def decode_file(path: str):

    headers = {}
    current_header = ""

    # Loop trough all lines of the .osu file
    for line in tools.read_file(path).split("\n"):
        # Strip the line so we wont have any additional spaces
        line = line.strip()
        # skip the line if the its is empty of if it starts with a //
        if not line or line.startswith("//"):
            continue

        # If the line starts with "[" and ends with "]" set the header into the object and skip the line
        if line.startswith('[') and line.endswith(']'):
            current_header = line.strip('[]')
            continue

        # For General and Difficulty headers assign the values in a object
        if current_header in ["General", "Difficulty"]:
            # Set the current header to be a empty object
            if not headers.get(current_header):
                headers[current_header] = {}

            # Function to make life easier
            def keyword_to_obj(str: str):
                key, value = str.split(":", 1)
                return key.strip(), tools.try_to_nr(value.strip())

            # Get the key and the value
            key, value = keyword_to_obj(line)

            # Assign the key and the value in the header
            headers[current_header][key] = value
            # Continue reading the rest of the lines
            continue

        if current_header in ["TimingPoints", "HitObjects"]:
            # Set the current header to be a empty object
            if not headers.get(current_header):
                headers[current_header] = []

            # Variable to store the line's values in an array
            line_vals = []

            # Loop trough the values of the line
            for val in line.strip().split(","):
                # Try to convert the strings to a number
                val = tools.try_to_nr(val)
                # Append the manipulated value to the line_vals
                line_vals.append(val)

            # Append the line_vals to the current header array
            headers[current_header].append(line_vals)

    # Return the object with the file values
    return headers


# Normalise the osu object incliding:
# 1. Add the slider multiplier to the timing points slider velocity
# 2. Normalise the hitSample of the HitObjects and limit them up to only 8 characters
# 3. Add empty strings between the timings notes (when there are no hitsounds so each ms will be defined by a string)
# 4.
#    a. For TimingPoints convert it into the next syntax:
#        from: time,beatLength,meter,sampleSet,sampleIndex,volume,uninherited,effects
#        to: bpm,sliderVelocity,meter,sampleSet,sampleIndex,volume,effects
#    b. For HitObjects
#        from:
#           x,y,time,type,hitSound,hitSample
#           x,y,time,type,hitSound,endTime,hitSample
#           x,y,time,type,hitSound,curveType|curvePoints,slides,length,edgeSounds,edgeSets,hitSample
#        to:
#           x,y,type,hitSound,endTime,curveType|curvePoints,slides,length,edgeSounds,edgeSets,hitSample
# 3. Convert the array of the HitObjects and TimingObjects back to strings
# 4. Return the HitObjects and TimingObjects
def normalise(osu, max_len):

    sliderMultiplier = osu["Difficulty"]["SliderMultiplier"]
    TimingObjects = []
    HitObjects = []

    # Loop trough each milisecond of the song
    for ms in range(0, max_len):

        # FOR EACH HITOBJECT
        ho = next((ho for ho in osu["HitObjects"] if ho[2] == ms), None)

        if ho:

            ho_norm = [ho[0], ho[1], ho[3], ho[4],
                       0, 0, 0, 0, 0, 0, ho[-1][:8]]

            match len(ho):
                # For circle there is nothging left to do.. the circle is already parsed
                case 7:  # Spinner
                    ho_norm[4] = ho[5]  # endTime
                case 11:  # Slider
                    # Assign: curveType|curvePoints,slides,length,edgeSounds,edgeSets
                    ho_norm[5:10] = ho[5:10]

            # Append the normalised hitObject
            HitObjects.append(",".join(str(value) for value in ho_norm))
        else:
            HitObjects.append("")

        # FOR TIMING POINTS
        # Check if there is a timepoint at this part of the milisecond
        tp = [tp for tp in osu["TimingPoints"] if tp[0] == ms]

        # If there is not timepoint and this is the first milisecond add an empty timepoint
        if not tp and not ms:
            TimingObjects.append("")
            continue
        # If there is no timepoint, append the previous timepoint
        if not tp:
            TimingObjects.append(TimingObjects[ms-1])
            continue

        if len(tp) == 1:
            # If there is only 1 timepoint (time points can be dublicated and overwritten)
            # append the normal values to meet the syntax
            tp = tp[0]
            tp_norm = [0, 0, tp[2], tp[3], tp[4], tp[5], tp[7]]
            if tp[6]:
                tp_norm[0] = tp[1]
            else:
                tp_norm[1] = tp[1] * sliderMultiplier
            TimingObjects.append(",".join(str(value) for value in tp_norm))
        else:
            # If there are multiple timepoints in the same milisecond apply the options of the last timepoint
            # as it overwrites everything from the previous timepoints
            tp_norm = [0, 0, tp[-1][2], tp[-1][3],
                       tp[-1][4], tp[-1][5], tp[-1][7]]

            # Loop trough the timepoints and append the bpm or slider velocity
            for tp_part in tp:
                # If its inhired timing point
                if tp_part[6]:
                    # Append bpm
                    tp_norm[0] = tp_part[1]
                else:
                    # Append the slider velocity x slider multiplier
                    tp_norm[1] = tp_part[1] * sliderMultiplier
            TimingObjects.append(",".join(str(value) for value in tp_norm))

    return TimingObjects, HitObjects
