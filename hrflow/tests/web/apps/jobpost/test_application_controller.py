

COVER_LETTER = '''
                        dear manager, 
                        
                        As a ML engineer I am highly interested in joining your startup and add direct value to your project
                        ....
                        '''

class TestApplicationController:
    
    
    def test_apply_for_jobpost(self, user_with_client,get_main_jobpost):
        newuser, client = user_with_client("newuser","password")
        res = client.post(
            f"/job/application/{get_main_jobpost.id}/{newuser.id}", 
            headers={"Authorization":f"Bearer {newuser.access_token}"}, 
            json={
                "cover_letter":COVER_LETTER
            })
        assert res.status_code == 202
        
    def test_get_applicants(self, mainuser_with_client, get_main_jobpost):
        user, client = mainuser_with_client
        res = client.get(f"/job/application/{get_main_jobpost.id}", headers={
            "Authorization":f"Bearer {user.access_token}"
        })
        
        assert res.status_code == 200 
        json_ = res.json()
        assert isinstance(json_,list)
        assert len(json_) == 1
        assert json_[0]['application_body']['cover_letter'] == COVER_LETTER
        assert json_[0]['post_id'] == get_main_jobpost.id
        
    # Authorization test
    def test_not_anyone_can_see_applicants(self, user_with_client, get_main_jobpost):
        user, client = user_with_client("newuser2", "password")
        res = client.get(f"/job/application/{get_main_jobpost.id}", headers={
            "Authorization":f"Bearer {user.access_token}"
        })
        
        assert res.status_code == 401
