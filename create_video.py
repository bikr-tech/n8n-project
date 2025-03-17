from moviepy.editor import *


def create_video_with_text(output_file, title, description, duration=5):
    """
    Creates a video with a title and description.

    Args:
        output_file (str): The output video file path.
        title (str): The title text.
        description (str): The description text.
        duration (int): The duration of the video in seconds.
    """

    # Create a blank clip
    clip = ColorClip(
        size=(1280, 720), color=(0, 0, 0), duration=duration
    )  # Black background

    # Create title text clip
    title_clip = TextClip(title, fontsize=70, color="white")
    title_clip = title_clip.set_position("center").set_duration(duration)

    # Create description text clip
    description_clip = TextClip(description, fontsize=30, color="gray")
    description_clip = description_clip.set_position(("center", 400)).set_duration(
        duration
    )  # place description below the title.

    # Composite the clips
    final_clip = CompositeVideoClip([clip, title_clip, description_clip])

    # Write the video file
    final_clip.write_videofile(output_file, fps=24)


# Example usage
create_video_with_text(
    "my_video.mp4", "My Video Title", "This is a sample description.", duration=10
)
