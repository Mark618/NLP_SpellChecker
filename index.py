from dash import Dash, html, dcc, callback, Output, Input,State
import dash_mantine_components as dmc
import os
import additional_func
import spacy
import additional_func
import pickle


CURRENT_DIR = os.getcwd()

def spacy_tokenize():    
    nlp = spacy.load("en_core_web_sm",exclude=["tok2vec","parser", "ner"])    
    return nlp

def detect_model():
    # Load NLTK language model
    with open(os.path.join(CURRENT_DIR,"model/model.pkl"),"rb") as p:
        model = pickle.load(p)        
    return model

def word_dict():
    # Get unique words
    with open(os.path.join(CURRENT_DIR,"data/processed_texts.pkl"),"rb") as p:
        word_list = pickle.load(p)    
        
    word_dict = {}
    for row in word_list:
        for word in row:
            if word not in word_dict:
                word_dict[word] = len(word)                
    return word_dict 

nlp = spacy_tokenize()
model = detect_model()
wl_process = word_dict()
spell_crrct_obj = additional_func.SpellCorrection(nlp,model) 



external_stylesheets = [os.path.join(CURRENT_DIR,'/assets/materialize.css'), 'https://fonts.googleapis.com/icon?family=Material+Icons']


app = Dash(external_stylesheets=external_stylesheets)
app.title = "Medical Spell Checker"    

app.layout = html.Div(
    [
        html.Nav(
            html.Div(
                className="nav-wrapper",
                children=[
                    html.A("Medical Spell Checker", className="brand-logo", style={"padding-left": "15px"},
                           href="/apps/home"),                    
                ],
                style={"backgroundColor": "Teal"}

            ),
        ),
        dcc.Location(id='url', refresh=False),
        
        html.Div(id='Content',className='row', children=[
            html.Div(id='Sidebar',className='container col s2',children=[
                html.H4("About the App"),
                html.P("A probabilistic model for detecting of spelling errors and correct spelling errors",style={'text-align': 'justify'}),
                html.P("Given a misspelled word, find the most likely correction(s) from a medical dictionary."),
                html.H5("Developed by"),
                html.P("Mick Yean Tuck Fei"),
                html.P("tp044713@mail.apu.edu.my",style={'text-align': 'justify'}),
                html.P("Mark Yean Tuck Ming"),
                html.P("tp044716@mail.apu.edu.my",style={'text-align': 'justify'})
            ]),

            
            html.Div(className='container col s10',children=[
                dcc.Markdown("""
                        #### Description
                        Check for spelling errors in medical and healthcare-related terms.Dictionary is restricted to biomedical terminology. Check is not case-sensitive. 
                        """),
                dcc.Markdown('___')
            ]),
            #Paste text to get spelling suggestions for though terms such as glaucoma , liver , heart glauasdcoma,liveer,herat
            html.Div(id='page-content', className='container col s10', children=[
                html.Div(className="input-field",children=[
                    html.H4("Input"),
                    dcc.Textarea(
                        id='textarea', className="materialize-textarea",
                        value='Paste text to get spelling suggestions for though terms such as glauasdcoma,liveer,herat', maxLength = 500,
                        style={'width': '100%', 'height': 250},
                    ),
                ]),
                html.Button('Check', id='check-button', className="waves-effect waves-light btn", n_clicks=0),
                
                html.Div(id='spelling-error',className='container col s10',children=[]),
                dcc.Store(id='ids-store'),                
                dcc.Store(id='real-ids'),
               
        
            ]),                
                
                      
            
        ]), 
    ]
)


@callback(
    Output('spelling-error', 'children', allow_duplicate=True),
    Output('ids-store','data'),   
    Input('check-button', 'n_clicks'),
    State('textarea', 'value'),
    prevent_initial_call=True    
)
def check_spell(n_clicks, value):
    if n_clicks >0:
        wrong_words,words_pos = spell_crrct_obj.detect_spell_error(value)        
        
        temp_sent = spell_crrct_obj.preproc_sent(value)
        
        if len(words_pos)==0:
            div_child_none = []
            div_child_none.append(html.P("No spelling error detected/ No match found."))
            div_child_none.append(html.Button('Next', id='submit-button', className="waves-effect waves-light btn", n_clicks=0))
            
            return div_child_none,[words_pos,temp_sent]
                
        else: 
            div_child =[]           
            div_child.append(html.H5("Result"))
            for i,word in enumerate(wrong_words):
                sorted_keys = spell_crrct_obj.possible_words(wl_process,word)
                
                section=html.Div(children=[                
                    html.H6(f"Found possible wrong words: {word[1]}"),
                    dcc.Dropdown(sorted_keys,placeholder="Dictionary",id=f'dropdown_{word[1]}')
                ])
                div_child.append(section)
            new_button = html.Button('Next', id='submit-button', className="waves-effect waves-light btn", n_clicks=0)
            div_child.append(html.Br())    
            div_child.append(new_button)  

            return div_child,[words_pos,temp_sent]


   
@callback(
    Output('textarea','value', allow_duplicate=True),
    # Output('spelling-error', 'children', allow_duplicate=True),
    Input("submit-button",'n_clicks'),
    State('spelling-error', 'children'),
    State('ids-store','data'),        
    prevent_initial_call=True
)
def get_dropdown_id(n_clicks,children,data):
    if n_clicks >0:
        ch_list = []
        word_pos=data[0]       
        temp_sent = data[1]
        if len(word_pos)!=0:
            for child in children:    
                if type(child['props']['children']) == list:            
                    word_sel=str(child['props']['children'][1]['props']['value'])
                    ch_list.append(word_sel) 
            for i,word in enumerate(ch_list):       
                temp_sent[word_pos[i]] =word
            
        new_sent = " ".join(temp_sent)        
        return f"{new_sent}"  
    
       
  
@callback(
    Output('spelling-error', 'children', allow_duplicate=True),
    Output('real-ids','data'),   
    Input("submit-button",'n_clicks'),
    Input('textarea', 'value'),
    prevent_initial_call=True
)
def check_real_erro(n_clicks,value):
    if n_clicks >0:        
        wrong_words,words_pos = spell_crrct_obj.detect_real_error(value)    
        
        temp_sent = spell_crrct_obj.preproc_sent(value)
        if len(words_pos) ==0:
            return(html.P("No spelling error detected/ No match found.")),[words_pos,temp_sent]        
        else: 
            div_child =[]           
            div_child.append(html.H5("Result"))
            for i,word in enumerate(wrong_words):
                sorted_keys = spell_crrct_obj.possible_words(wl_process,word)
                
                section=html.Div(children=[                
                    html.H6(f"Found possible wrong words: {word[1]}"),
                    dcc.Dropdown(sorted_keys,placeholder="Dictionary",id=f'dropdown_{word[1]}')
                ])
                div_child.append(section)
            new_button = html.Button('Submit', id='real-submit-button', className="waves-effect waves-light btn", n_clicks=0)
            div_child.append(html.Br())    
            div_child.append(new_button)  

            return div_child,[words_pos,temp_sent]   
    
    
@callback(
    Output('textarea','value', allow_duplicate=True),    
    Output('spelling-error', 'children', allow_duplicate=True),
    Input("real-submit-button",'n_clicks'),
    State('spelling-error', 'children'),
    State('real-ids','data'),        
    prevent_initial_call=True
)
def get_real_dropdown_id(n_clicks,children,data):
    if n_clicks >0:
        ch_list = []
        word_pos=data[0]       
        temp_sent = data[1]  
        if len(word_pos)!=0:      
            for child in children:    
                if type(child['props']['children']) == list:            
                    word_sel=str(child['props']['children'][1]['props']['value'])               
                    ch_list.append(word_sel) 
            
            for i,word in enumerate(ch_list):                
                temp_sent[word_pos[i]] =word
            
        new_sent = " ".join(temp_sent)       
        return f"{new_sent}", html.Br(children=[])    

if __name__ == '__main__':
    app.run(debug=True)
