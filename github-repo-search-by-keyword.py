#!/usr/bin/env python3.10.6
# -*- coding: utf-8 -*-

# run script from command line via python3 github-repo-search-by-keyword.py

import click
import csv
import datetime
import time
# This script uses PyGithub library. To learn more: https://pygithub.readthedocs.io/en/stable/
from github import Github
from github.GithubException import RateLimitExceededException
from tqdm import tqdm


def search_github(auth: Github, organization:str, keyword: list) -> list:
    """Search the GitHub API for repositories using an input keyword.

    Args:
        auth: A Github authenticate object.
        keyword: A keyword string.

    Returns:
        A nested list of GitHub repositories returned for a keyword. Each result list contains the repository name,
        url, and description.
    """

    print('Searching GitHub using keyword: {}'.format(keyword))
    # set-up query to saerch repos using keywords in an organization
    # keyword is searched in the repo name and description by default. if you want to search the keyword in the README append 'in:readme+in:description' to the query
    # to search repos within a specific organization, edit the 'org:{org-name}' in the query
    # if no org is specified remove the 'org:{org-name}' from the query
    # the query below searches for the forked repos additionaly. it is optional but use it to get all the related repos.
   
    if(organization == ''):
        query = keyword + 'fork:true:'
    query =keyword + 'fork:true:' + organization
    results = auth.search_repositories(query, 'stars', 'desc')

     # set-up query to saerch all the repos a team owns using the team id - comment down the lines above to use the team based search down below
   
    # To learn the team ID without admin rights, just go to https://github.com/orgs/<org-name>/teams/<team-name> in your browser and alt-click the avatar image to copy its address.
    # The avatar will be stored at https://avatars3.githubusercontent.com/t/1234567?s=280&v=4 -- where 1234567 is that team ID.

    # org = auth.get_organization(organization)
    # results = org.get_team(1234567).get_repos()
    
    print(f'Found {results.totalCount} repo(s)')

    results_list = []
    for repo in tqdm(range(0, results.totalCount)):
        try:
            try :  
        
                isLicenseName = results[repo].get_license().license.name 
                isLicenseURL = results[repo].get_license().license.url 

                topics = results[repo].get_topics()
                topicsList = str(topics)
                
            except: 
               isLicenseName = "N/A"
               isLicenseURL = "N/A"
            # Internal info is the URL for that specific repo in Microsoft's Internal Open Source Management system. 
            # If you're an authorized user, you can see the direct owners, security groups and internal metadata about the repo.
            # To search within an organization other than 'Azure', don't forget to edit the URL below accordingly.
            internalInfo = "https://repos.opensource.microsoft.com/orgs/Azure/repos/"+results[repo].name
            results_list.append([results[repo].id, results[repo].name,results[repo].html_url, results[repo].description, results[repo].visibility, results[repo].archived, results[repo].stargazers_count, isLicenseName, isLicenseURL, results[repo].updated_at, results[repo].open_issues_count, topicsList, internalInfo])
            time.sleep(2)
        except RateLimitExceededException:
            time.sleep(60)
            results_list.append([results[repo].id, results[repo].name,results[repo].html_url, results[repo].description, results[repo].visibility, results[repo].archived, results[repo].stargazers_count, isLicenseName, isLicenseURL, results[repo].updated_at, results[repo].open_issues_count, topicsList, internalInfo])

    return results_list


@click.command()
@click.option('--token', prompt='Please enter your GitHub Access Token')
@click.option('--organization', prompt='Please enter the organziation name in GitHub you want to search repos in. If you do not want to specify an org, leave it blank and hit Enter ', default="")
@click.option('--keywords', prompt='Please enter the keywords separated by a comma')
@click.option('--filename', prompt='Please provide the path of the .csv file you want to save results to')
def main(token: str, organization:str, keywords: str, filename: str) -> None:

    # initialize and authenticate GitHub API
    auth = Github(token)
    # search a list of keywords
    search_list = [keyword.strip() for keyword in keywords.split(',')]

    # search repositories on GitHub
    github_results = dict()
    for key in search_list:
        github_results[key] = []
        github_results[key] += search_github(auth, organization, key)
        if len(search_list) > 1: time.sleep(5)

    # read existing CSV file to check for duplicates
    existing_results = set()
    try:
        with open(filename, 'r') as f_in:
            reader = csv.DictReader(f_in)
            for row in reader:
                existing_results.add(row['ID'])
    except FileNotFoundError:
        raise FileNotFoundError

    # write out new results to the same CSV file
    timestamp = datetime.datetime.now()
    formatted_date = timestamp.strftime('%d') + timestamp.strftime('%b') + timestamp.strftime('%Y')
    # if you want to create a .csv from scratch uncomment the line below
    # full_filename = filename.strip() + 'GitHub_Search_Results_' + formatted_date + '.csv'
    # if you already created a .csv just provide the full path when you run the script
    full_filename = filename
    print('Writing search results to: {}'.format(full_filename))
   
    with open(full_filename, 'a', newline='') as f_out:
        writer = csv.writer(f_out)
        if f_out.tell() == 0:
            writer.writerow(['Keyword','ID', 'Name', 'URL', 'Description','Visibility','Archived','Stars','License-Name','License-URL','Updated-At', 'Open-Issue-Number', 'Topics', 'Info & Contact'])
        for key in tqdm(github_results.keys()):
            for res in github_results[key]:
                if str(res[0]) in existing_results: continue

                writer.writerow([key, res[0], res[1], res[2],res[3], res[4], res[5], res[6], res[7], res[8], res[9], res[10], res[11], res[12]])
                existing_results.add(str(res[0]))

    f_out.close()


if __name__ == '__main__':
    main()