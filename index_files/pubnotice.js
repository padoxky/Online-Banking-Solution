function Notice(text, url, ispublic, start, expiry, iskiosk)
{
this.text = text;
this.url = url;
this.ispublic = ispublic;
this.start = start;
this.expiry = expiry;
this.iskiosk = iskiosk;
}
numberofnotices=1;
notices = new Array(numberofnotices);
notices[0] =  new Notice("Technical Advisory: RBC Direct Investing Account Open Application and eSubmission forms currently unavailable.","/onlinebanking/bankingusertips/notices/di_account_open.html",true,"20110601","20110603",true);
