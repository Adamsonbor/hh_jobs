class Processor:
    def __init__(self):
        self.data = []
        self.idxs = []


    def is_not_null(json, param):
        return True if param in json.keys() else False


    def get_param(self, json, *params):
        try:
            for param in params:
                json = json[param]
            return json
        except:
            return None


    def key_skills(self, json):
        try:
            return [item["name"] for item in json["key_skills"]]
        except:
            return None


    def specializations(self, json):
        try:
            ids = [item["id"].split(".")[-1] for item in json["specializations"]]
            names = [item["name"] for item in json["specializations"]]
            profarea_ids = [int(item["profarea_id"]) for item in json["specializations"]]
            profarea_names = [item["profarea_name"] for item in json["specializations"]]
            out = []
            for item in zip(ids, names, profarea_ids, profarea_names):
                out.append({"specialization_id":item[0], "specialization_name":item[1],
                            "profarea_id":item[2], "profarea_name":item[3]})
            return out
        except:
            return None

    
    def professional_roles(self, json):
        try:
            ids = [item["id"] for item in json["professional_roles"]]
            names = [item["name"] for item in json["professional_roles"]]
            out = []
            for role in zip(ids, names):
                out.append({"professional_role_id":role[0], "professional_role_name":role[1]})
            return out
        except:
            return None, None
    

    def set_idxs(self, json):
        self.idxs = tuple(vacancy["id"] for vacancy in json)


    def __call__(self, json):
        self.data = []
        for item in json:
            data = {}
            data["id"] = self.get_param(item, "id")
            data["name"] = self.get_param(item, "name")
            data["area_id"] = self.get_param(item, "area", "id")
            data["area_name"] = self.get_param(item, "area", "name")
            data["salary_from"] = self.get_param(item, "salary", "from")
            data["salary_to"] = self.get_param(item, "salary", "to")
            data["type"] = self.get_param(item, "type", "name")
            data["department_id"] = self.get_param(item, "department", "id")
            data["department_name"] = self.get_param(item, "department", "name")
            data["address"] = self.get_param(item, "address", "raw")
            data["contacts"] = self.get_param(item, "contacts")
            data["experience"] = self.get_param(item, "experience", "name")
            data["schedule"] = self.get_param(item, "schedule", "name")
            data["employment"] = self.get_param(item, "employment", "name")
            data["key_skills"] = self.key_skills(item)
            data["specializations"] = self.specializations(item)
            data["professional_roles"] = self.professional_roles(item)
            data["employer_id"] = self.get_param(item, "employer", "id")
            data["employer_name"] = self.get_param(item, "employer", "name")
            data["created_at"] = self.get_param(item, "created_at")
            data["description"] = self.get_param(item, "description")
            self.data.append(data)
        self.set_idxs(self.data)
        return self.data

    
    def __getitem__(self, idx):
        return self.data[idx]


