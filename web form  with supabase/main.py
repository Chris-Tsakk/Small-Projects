import os
from datetime import datetime
from supabase import create_client, Client
import pytz
from dotenv import load_dotenv
from fasthtml.common import *




#env variable
load_dotenv()

TIMESTAMP_FMT = "%Y-%m-%d %I:%M:%S %p GMT"
#int supabase
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

app, rt = fast_app()

def get_gmt_time():
    gmt_tz=pytz.timezone("GMT")
    return datetime.now(gmt_tz)

def add_message(name,message):

    timestamp = get_gmt_time().strftime(TIMESTAMP_FMT)
    data = {"name": name, "message": message, "timestamp": timestamp}
    print("Inserting:", data)  # Debugging print

    response = supabase.table("App").insert(data).execute() # insert data to supabase
    print("Response:", response)


       # {"name":name, "message":message, "timestamp":timestamp}
    #).execute()

def get_message():
    #sort my id
    response= supabase.table("App").select("*").order("id",desc=True).execute()
    return response.data



def render_message(entry):
    return Article(
        Header(f"Name: {entry['name']} "),
        P(entry["message"]),
        Footer(Small(Em(f"Posted: {entry['timestamp']}"))),
    )

def render_message_list():
    messages = get_message()#[
        #{"name": "Peter", "message": "Hello!", "timestamp": "tonight"},
       # {"name": "lek", "message": "How are you?", "timestamp": "tonight"},
   # ]
    return Div(
        *[render_message(entry) for entry in messages],
        id="message-list"
    )

def render_content():
    form = Form(
        Fieldset(
            Input(
                type="text",
                name="name",
                placeholder="name",
                required=True,
                maxlength=20,
            ),
            Input(
                type="text",
                name="message",
                placeholder="message",
                required=True,
                maxlength=40,
            ),
            Button("Done", type="submit"),
        ),
        method="post",
        hx_post="/submit-message",
        hx_target="#message-list",
        hx_swap="outerHTML",
        hx_on__after_request="this.reset()",

    )


    return Div(
        P(Em("This is first")),
        form,
        P("form is here"),
        Div(
            "This is created with",
            A("Sakura", href="https://sekura-global.com/", target="_blank"),
            Hr(),
            render_message_list(),
            P("this is a paragraph line "),
        )
    )

@rt("/")
def get():
    return Titled("The form", render_content())


@rt("/submit-message", methods=["POST"])
def post(name: str , message:str ):
    add_message(name,message)
    return render_message_list()

serve()