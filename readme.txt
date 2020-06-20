Instruction

1. Read this instruction
2. Install Python
3. Install Selenium
4. Install FireFox
5. Install geckodriver for FireFox
6. Specify testLogin and testPwd variables inside the test02.py (lines 11 & 12)
   * Please note that URL is hardcoded inside the script
7. Run test02.py using Python
8. Enjoy the result
   ** Please note that expected result is "provider created"
      but actual result is "error_you_are_not_allowed_to_save_provider_..."
   *** Please note that only required field are populated
   **** Please note that provider login and email which are probably unique across users
        are not auto-generated but rather specified in the test data inside the script.
  	So if first run was successfull and second run is required
        one must either re-deply the DB dump or change the test data inside the script
        or delete previously inserted provider info. 
	Otherwise unique key violation error is possible.

2020-06-20 11:13