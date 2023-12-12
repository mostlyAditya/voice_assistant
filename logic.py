import speech_synthesis
import transcriber


def to_take_notes(response):
    if (("take" in response.lower()) or ("make" in response.lower())) and ("note" in response.lower()):
        print("Taking a note")
        return True
    return False

def to_book_meeting(response):
    if ("book" in response.lower()) and ("meeting" in response.lower()):
        print("Booking a meeting room")
        return True
    return False

def anything_else_audio():
    expression = "Anything else?"
    speech_synthesis.play_text(expression)
    return 

def uh_huh_response():
    expression = "uh huh!"
    speech_synthesis.play_text(expression)
    return 

def start_response():
    expression = "I am listening"
    speech_synthesis.play_text(expression)
    return 

def default_response():
    expression = "I did not get you!"
    speech_synthesis.play_text(expression)
    return

def book_meeting():
    booked_response = "Alright I have booked this meeting room for you!"
    speech_synthesis.play_text(booked_response)
    print("Room Booked")
    return 

def notes_logic():
    note_text = transcriber.transcribe(chunk_length_s=5.0, stream_chunk_s=1.0)
    print(f"Note: {note_text}")
    anything_else_audio()
    note_count = 0
    while True:
        if note_count > 0:
            uh_huh_response()
        response = transcriber.transcribe(chunk_length_s = 5.0, stream_chunk_s = 1.0)
        if "that's enough" in response.lower():
            break
        else:
            note_text = response
            print(note_text)
            note_count += 1


def main():
    print("Transcription Started")
    start_response()
    transcription = transcriber.transcribe(chunk_length_s=5.0, stream_chunk_s = 1.0)
    print("This was heard -- ", transcription)

    if to_book_meeting(transcription):
        book_meeting()
        pass
    elif to_take_notes(transcription):
        uh_huh_response()
        notes_logic()
        pass
    else:
        default_response()



