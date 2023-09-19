from glob import glob
import os
import json
from pathlib import Path

import tyro
import cv2

def get_video_paths(video_dir: Path) -> list[str]:
    """Get all video paths in video_dir"""
    assert video_dir.exists(), f"Video directory {video_dir} does not exist"
    video_paths = sorted(glob(str(video_dir) + '/*.mp4'))
    assert len(video_paths) > 0, f"No video found in {video_dir}"

    return video_paths

def stream_video(video_path) -> None:
    """stream video from video_path"""
    cap = cv2.VideoCapture(video_path)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        yield frame
    cap.release()


def run(video_dir: Path) -> None:
    """Show video and save labels to file, can choose between 2 classes, use space bar or q, default is q"""
    save_file = video_dir / 'labels.json'
    assert not save_file.exists(), f"Labels file {save_file} already exists!"

    labels = []
    video_paths = get_video_paths(video_dir)
    for video_path in video_paths:
        label = {
            'video_path': video_path,
            'space_bar': "false"
        }

        for frame in stream_video(video_path):
            cv2.imshow('frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            if cv2.waitKey(1) & 0xFF == ord(' '):
                label['space_bar'] = "true"
                break
                
        print(f"{label=}")
        labels.append(label)
        cv2.destroyAllWindows()

    print(f"Saving labels for {video_path} to file {save_file}")
    with open(save_file, 'w') as f:
        json.dump(labels, f, indent=4)


if __name__ == "__main__":
    tyro.cli(run)
