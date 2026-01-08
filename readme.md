### main_streamlit.py
- check if vector db exist?
  - if 
        yes then load the existing one 
  - else
        check dataset is in docs folder
        if yes 
              then create chunks->embed->create vector db by using chroma vector db
        else
             raise error that no files are their 

- give query PRESS ENTER 
->bot give answer 
-> also show retrive chunks he got .

other key features: in prompt aslo giving last 3 chat turns to bot 
                    so that it can answer follow up queries more better
                    