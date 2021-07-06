from logging import setLoggerClass
from os import name
from flask import Flask
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

class Applications:
    def __init__(self):
        self.stages = ['Assessment', 'Preliminary Phone Screen', 
        'Hiring Manager Review', 'Phone Interview 2', 'Application Review', 'Case Study & Task', 'Case Study', 'Executive Review', 
        'Technical Interview', 'HR Discussion', 'Recruiter Evaluation', 'Phone Interview', 'Offer Short List', 
        'Panel Screening', 'Take Home Test', 'HR Round', 'Offer', 'Hiring Manager Interview', 'Recruiters Evaluation', 
        'Executive Interview', "Recruiter's Evaluation", 'HR Interview', 'Face to Face']
        self.allData = {}
        self.active = {}
        self.hired = {}
        self.rejected = {}
        self.jobs_list_ids = {}
        self.jobs_list_names = {}
        self.number_of_applicants_per_job_id = {}
        self.jobIdData = []

    def application_processing(self, jobs_list_ids,jobs_list_names, apps):
        self.jobs_list_ids = jobs_list_ids
        self.jobs_list_names = jobs_list_names
        if apps:
            for app in apps:
                
                applied_job_id = app['jobs'][0]['name']
                if(applied_job_id in self.number_of_applicants_per_job_id.keys()):
                    self.number_of_applicants_per_job_id[applied_job_id] += 1
                else:
                    self.number_of_applicants_per_job_id[applied_job_id] = 1
                if(app['status'] == 'hired'):
                    if(applied_job_id in self.hired.keys()):
                        self.hired[applied_job_id] += 1
                    else:
                        self.hired[applied_job_id] = 1
                    
                elif(app['status'] == 'rejected'):
                    if(applied_job_id in self.rejected.keys()):
                        self.rejected[applied_job_id] += 1
                    else:
                        self.rejected[applied_job_id] = 1
                elif(app['status'] == 'active'):
                    if(applied_job_id in self.active.keys()):
                        self.active[applied_job_id] += 1
                    else:
                        self.active[applied_job_id] = 1

    def getTable(self, jobs_list_ids, jobs_list_names):
        for job_id, job_name in zip(jobs_list_ids, jobs_list_names):
            temp = {'Id': job_id, 'Name':job_name, 'Active': 0, 'Rejected': 0, 'Hired': 0}
            if(job_name in self.active.keys()):
                temp['Active'] = self.active[job_name]
            if(job_name in self.rejected.keys()):
                temp['Rejected'] = self.rejected[job_name]
            if(job_name in self.hired.keys()):
                temp['Hired'] = self.hired[job_name]
            self.jobIdData.append(temp)

    
                

    def getTemplatejson(self):
        final = {}
        for stage in self.stages:
            final[stage] = {'active': 0, 'hired': 0, 'converted': 0, 'rejected': 0}
        return final

    def newApplication_processing(self, jobs_ids, jobs_names, apps):
        self.jobs_list_ids = jobs_ids
        self.jobs_list_names = jobs_names
        # if apps:
        #     for app in apps:
        #         applied_job_id = app['jobs'][0]['id']

        #         if(applied_job_id not in self.allData.keys()):
        #             templatejson = self.getTemplatejson()
        #             self.allData[applied_job_id] = templatejson
        #         if(app['current_stage'] and app['status']):
        #             self.allData[applied_job_id][app['current_stage']['name']][app['status']] += 1
        if apps:
            for app in apps:
                applied_job_name = app['jobs'][0]['name']
                # applied_job_id = app['jobs'][0]
                if(applied_job_name not in self.allData.keys()):
                    templatejson = self.getTemplatejson()
                    self.allData[applied_job_name] = templatejson
                if(app['current_stage'] and app['status']):
                    self.allData[applied_job_name][app['current_stage']['name']][app['status']] += 1
        
                          
    
def create_json(o1):
    myDict = {'jobs_list_IDs': o1.jobs_list_ids,
            'jobs_list_Names': o1.jobs_list_names,
            'Number of Applicants per job': o1.number_of_applicants_per_job_id,
            'Rejected': o1.rejected, 
            'Active': o1.active,
            'Hired': o1.hired}
    return myDict

# @app.route('/getData')
# def get_data_application():
#     f = open("applications.txt", "r", encoding='utf-8', errors='ignore')
#     l = f.read()
#     fin = eval(l)
#     names = []
#     ids = []
#     for app in fin:
#         names.append(app['jobs'][0]['name'])
#         ids.append(app['jobs'][0]['id'])
#     ids = list(set(ids))
#     names = list(set(names))
#     o1 = Applications()
#     o1.application_processing(ids, names, fin)
#     return create_json(o1)

@app.route('/getTable')
def getTable():
    f = open("applications.txt", "r", encoding='utf-8', errors='ignore')
    l = f.read()
    fin = eval(l)
    f_jobs = open("jobs.txt", "r", encoding='utf-8', errors='ignore')
    l_jobs = f_jobs.read()
    fin_jobs = eval(l_jobs)
    names_jobs = []
    ids_jobs = []
    for job in fin_jobs:
        if(job['status'] == 'open'):
            names_jobs.append(job['name'])
            ids_jobs.append(job['id'])
    ids_jobs = list(set(ids_jobs))
    names_jobs = list(set(names_jobs))
    o1 = Applications()
    o1.application_processing(ids_jobs, names_jobs, fin)
    o1.getTable(ids_jobs, names_jobs)
    # print(o1.jobIdData)
    return {'data' : o1.jobIdData}


@app.route('/getDataFunnel')
def get_data_application():
    f = open("applications.txt", "r", encoding='utf-8', errors='ignore')
    l = f.read()
    fin = eval(l)
    f_jobs = open("jobs.txt", "r", encoding='utf-8', errors='ignore')
    l_jobs = f_jobs.read()
    fin_jobs = eval(l_jobs)
    names_jobs = []
    ids_jobs = []
    for job in fin_jobs:
        if(job['status'] == 'open'):
            names_jobs.append(job['name'])
            ids_jobs.append(job['id'])
    ids_jobs = list(set(ids_jobs))
    names_jobs = list(set(names_jobs))
    o1 = Applications()
    # o1.application_processing(ids_jobs, names_jobs, fin)
    o1.newApplication_processing(ids_jobs, names_jobs, fin)
    # return create_json(o1)
    return o1.allData

@app.route('/getData')
def get_total_application():
    f = open("applications.txt", "r", encoding='utf-8', errors='ignore')
    l = f.read()
    fin = eval(l)
    f_jobs = open("jobs.txt", "r", encoding='utf-8', errors='ignore')
    l_jobs = f_jobs.read()
    fin_jobs = eval(l_jobs)
    names_jobs = []
    ids_jobs = []
    for job in fin_jobs:
        if(job['status'] == 'open'):
            names_jobs.append(job['name'])
            ids_jobs.append(job['id'])
    ids_jobs = list(set(ids_jobs))
    names_jobs = list(set(names_jobs))
    o1 = Applications()
    o1.application_processing(ids_jobs, names_jobs, fin)
    return create_json(o1)

@app.route('/getJobNames') 
def get_job_names():
    f_jobs = open("jobs.txt", "r", encoding='utf-8', errors='ignore')
    l_jobs = f_jobs.read()
    fin_jobs = eval(l_jobs)
    names_jobs = []
    ids_jobs = []
    for job in fin_jobs:
        if(job['status'] == 'open'):
            names_jobs.append(job['name'])
            ids_jobs.append(job['id'])
    ids_jobs = list(set(ids_jobs))
    names_jobs = list(set(names_jobs))
    return {"jobNames" : names_jobs}

# @app.route('/getDataJobs')
# def get_Data_jobs():
#     f = open("jobs.txt", "r", encoding='utf-8', errors='ignore')
#     l = f.read()
#     fin = eval(l)


# app.debug = True
if __name__ == "__main__":
    app.run(debug=True, host='localhost', port=5000)