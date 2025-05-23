# Canal Product Resync Bot

This script solves a problem with product data being outdated between the Canal & Flip Shop platforms. 
As a solution, it automatically resyncs all product data from Canal >> Flip via the Canal API based on a daily-generated list of product IDs sourced from Looker and written to a Google Sheet (I wasn't able to use the Looker API because it caps returned data at 5k rows).
The data from Looker represents all of the products on the Flip platform currently integrated via Canal. 

## Overview

I set up a Looker report to automatically populate a Google Sheet with the product IDs for every product in Canal so that this script has an automated source for the data to be resynced. It then authenticates with the Google Sheets API using a service account, loads every product ID from the sheet into the payload of a POST request sent to Canal's `/resync` endpoint. This is scheduled to run dailiy at 21:55pm by a plist and executed via launchd on a Mac environment.