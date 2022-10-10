"""
Combines Coffea processor output pickle files

Author(s): Raghav Kansal
"""

import os
from os import listdir
import argparse
import pickle
from coffea.processor.accumulator import accumulate
import sys
from tqdm import tqdm


import sys

# needed to import run_utils from parent directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

import run_utils


def accumulate_files(files: list):
    """accumulates pickle files from files list via coffea.processor.accumulator.accumulate"""

    with open(files[0], "rb") as file:
        out = pickle.load(file)

    for ifile in tqdm(files[1:]):
        with open(ifile, "rb") as file:
            out = accumulate([out, pickle.load(file)])

    return out


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--indir",
        default="outfiles",
        help="eos directory which contains files to combine",
        type=str,
    )
    parser.add_argument("--name", default="", help="name of combined files", type=str)
    run_utils.add_bool_arg(
        parser, "r", default=False, help="combine files in sub and subsubdirectories of indir"
    )
    args = parser.parse_args()

    indir = f"/eos/uscms/store/user/rkansal/{args.indir}"

    files = [indir + "/" + file for file in listdir(indir) if file.endswith(".pkl")]

    if args.r:
        dirs = [indir + "/" + d for d in listdir(indir) if os.path.isdir(indir + "/" + d)]
        print(dirs)

        for d in dirs:
            files += [d + "/" + file for file in listdir(d) if file.endswith(".pkl")]
            subdirs = [d + "/" + sd for sd in listdir(d) if os.path.isdir(d + "/" + sd)]
            for sd in subdirs:
                files += [sd + "/" + file for file in listdir(sd) if file.endswith(".pkl")]

    print(f"Accumulating {len(files)} files")
    out = accumulate_files(files)

    name = args.name if args.name != "" else f"combined"

    with open(f"{indir}/{name}.pkl", "wb") as f:
        pickle.dump(out, f)

    print(f"Saved to {indir}/{name}.pkl")
