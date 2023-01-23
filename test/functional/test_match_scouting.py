import json

def test_scouting_form_get(test_client):
    response = test_client.get('/matches')
    assert response.status_code == 200

def test_scouting_form_post(test_client):
    """
    GIVEN a well formed match result  
    WHEN a Match result is posted 
    THEN check that the match is inserted correctly 
    """
    mimedata = "application/json"
    headers = {
        'Content-Type' : mimedata,
        'Accept' : mimedata
    }
    match_data =  {
		'matchNumber': 420,
		'teamNumber': 69,
		'alliance': "",
		'autonomous': { 'mobility': False, 'charge': 1 },
		'endgame': { 'charge': 2 },
		'win': False,
		'notes': "👌👌👌👌",
		'scoreMatrix': { 
            'high': [0,1,0,0,0,0,1,0,0],
            'mid':  [0,1,2,0,0,0,1,0,0],
            'low':  [0,1,0,0,2,0,1,0,0] 
        }
	}
    response = test_client.post('/matches',data=json.dumps(match_data),headers=headers)
    assert response.status_code == 200