# News Report
##Source code for the News Report.

**What you need:**
 >The linux VM

 >Vagrant installed on the VM

 >Postgreql installed

 >The news database available on the VM, you can check that by typing psql news, if you get an error then you need to download the database file [newsdata.sql](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip) and import it by typing psql -d news -f newsdata.sql into your terminal.


**How to use this:**
 >From the terminal navigate to the location of the project
 
 >Type vagrant up
 
 >Type vagrant ssh

 >cd into /vagrant

 >Add the code folder inside the vagrant folder on the VM

 >cd into the directory where the code is, which should be inside the VM
 
 >Type python news_forum.py, this will open a web page with the results in 
 it on the localhost:8000
 
 >Open the directory you will find a file called result.csv that contains the
  result of the sql queries

  >You can also type python in the terminal

  >import newsdb as n

  >Then type n.get_three_most_popular_articles()

  >Then type n.get_authors()

  >Then type n.get_errors()


  

