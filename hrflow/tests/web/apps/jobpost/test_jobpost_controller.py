

from hrflow.web.apps.jobpost.schema import JobPostRes


class TestJobPostController:
    
    def test_create_jobpost(self, mainuser_with_client):
        user, client = mainuser_with_client
        res = client.post(f"/job/post/{user.id}", json={
            "title":"Senior Software Engineer",
            "body":"Looking for python expert"
        },
        headers={
            "Authorization":f"Bearer {user.access_token}"
        })
        assert res.status_code == 201
        return JobPostRes(**res.json())

    def test_get_jobpost(self, mainuser_with_client):
        user, client = mainuser_with_client
        jbpost = self.test_create_jobpost(mainuser_with_client=mainuser_with_client)
        self._get_jobpost_by_id(client,jbpost.id, user.access_token)
    
    def test_modify_jobpost(self, mainuser_with_client):
        user, client = mainuser_with_client
        jbpost = self.test_create_jobpost(mainuser_with_client=mainuser_with_client)
        new_title = "Modified Senior Software Engineer"
        new_body = "Modified: Looking for python expert"
        res = client.put(f"/job/post/{jbpost.id}",
                    json={
                        "title":new_title,
                        "body":new_body
                    },
                    headers={
                    "Authorization":f"Bearer {user.access_token}"
            })
        assert res.status_code == 200
        modified_jbpost = self._get_jobpost_by_id(client,jbpost.id, user.access_token)
        assert modified_jbpost.title == new_title
        assert modified_jbpost.body == new_body
        
    def test_get_all_jobpost(self, mainuser_with_client):
        user, client = mainuser_with_client
        res = client.get(f"/job/post/",
                           headers={
            "Authorization":f"Bearer {user.access_token}"
        })
        assert res.status_code == 200
        json_ = res.json()
        assert isinstance(json_,list)
        assert len(json_) > 1
        
    def test_delete_jobpost(self, mainuser_with_client):
        user, client = mainuser_with_client
        jbpost = self.test_create_jobpost(mainuser_with_client=mainuser_with_client)
        self._get_jobpost_by_id(client,jbpost.id, user.access_token)
        res = client.delete(f"/job/post/{jbpost.id}", 
                            headers={
                                "Authorization": f"Bearer {user.access_token}"
                            })
        
        assert res.status_code == 204
        
    def test_interact_with_unfound_jobpost(self, mainuser_with_client):
        user, client = mainuser_with_client
        headers = {
            "Authorization":f"Bearer {user.access_token}"
        }
        res = client.get(f"/job/post/10000",headers=headers)
        assert res.status_code == 404
        res = client.delete(f"/job/post/10000",headers=headers)
        assert res.status_code == 404       
        res = client.put(f"/job/post/10000",json={"title":"title","body":"body"},headers=headers)
        assert res.status_code == 404
        
    # Authorization Tests
   
    def test_create_ajobpost_and_action_it_by_someone_else(self, mainuser_with_client, user_with_client):
        user, client = mainuser_with_client
        jbpost = self.test_create_jobpost(mainuser_with_client=mainuser_with_client)
        otheruser, client = user_with_client("otheruser", "hispassword")
        headers = {
            "Authorization":f"Bearer {otheruser.access_token}"
        }
        #You can see it
        res = client.get(f"/job/post/{jbpost.id}",headers=headers)
        assert res.status_code == 200
        #You cannot delete it 
        res = client.delete(f"/job/post/{jbpost.id}",headers=headers)
        assert res.status_code == 401       
        #You cannot update it
        res = client.put(f"/job/post/{jbpost.id}",json={"title":"title","body":"body"},headers=headers)
        assert res.status_code == 401

    def _get_jobpost_by_id(self,client,post_id, access_token)->JobPostRes:
        res = client.get(f"/job/post/{post_id}",
                           headers={
            "Authorization":f"Bearer {access_token}"
        })
        assert res.status_code == 200
        jbpost = JobPostRes(**res.json())
        assert res.json()['id'] == post_id
        return jbpost