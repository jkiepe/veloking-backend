import uvicorn
# from app.data.datamanager import DataManager

# data_manager = DataManager()
# user = {
#     "email": "jkiepe@inkontor.com",    
#     "firstName": "Jonasz",
#     "lastName": "Kiepe",
#     "rentalPoint": "baza",
#     "role": "manager",
#     "password": "Lucky786",
#     }
# data_manager.add_user(user)

if __name__ == "__main__":
    uvicorn.run("app.api:app", host="0.0.0.0", port=8081, reload=True)
