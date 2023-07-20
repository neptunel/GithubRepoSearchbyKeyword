# Search Github Repositories using Keywords

This script is created to search repositories in GitHub using set of keywords. It uses the [PyGitHub](https://pygithub.readthedocs.io/en/latest/index.html), a Python library to access the GitHub REST API.
Run script from command line via:  `python3 github-repo-search-by-keyword.py`

Make sure to install the dependecies via pip: `pip3 install click csv datetime time Github tqdm`

Script will ask for command line inputs such as: 
 - **GitHub Acess Token:** You need a GitHub account to generate a token, make sure it is not expired and you added the required scopes and authenticated to the organizations you wanted to apply search. To learn how to create a token, visit the [official document](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens).
 - **Organization Name:** This is an optional step. If you want to search repositories under a specific organization, make sure to type the organziation name exactly how it is in GitHub. If you don't want to specify an org hit enter, and it'll search the keywords in the entire GitHub. GitHub REST API provides up to 1,000 results for each search. You can narrow your search using queries. To learn more about the search query syntax, see [Search](https://docs.github.com/en/rest/search?apiVersion=2022-11-28#constructing-a-search-query).
 - **Keywords:** Create s dictionary of keywords seperated by commas if you search more than a word. The Search API is case insensitive.
 - **Path of the .csv file:** Create a file with .csv extension to get search results to saved into. You can use the same file to perform multiple search by running the script again. It'll append the new repositories to the existing ones, and it'll prevent duplicating the repositories if it already exists in the .csv.

You can specify the search by adding filters to the query string. You can also search topics, users, code, issues etc. To see which methods PyGithub provides, check [Search API reference](https://pygithub.readthedocs.io/en/latest/github.html#github.MainClass.Github.search_repositories).
In the script at line 45, there's an example of how to search all the visible(non-secret) repositories a team has using the Team ID. You need to provide an organization input, if you want to search a team's repositories. In additon to the comment about finding the Team ID, you can visit https://repos.opensource.microsoft.com/orgs/<org-name>/teams/<team-name> and find the Team ID at the bottom of the page.