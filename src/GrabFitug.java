/**
 * @author Bernd Fix <bernd@wauland.de>, 2000-2012
 * @author Hernani Marques <h2m@access.uzh.ch>, 2012 (minimal changes)
 */

package wht4;

import java.net.*;
import java.io.*;
import java.sql.Date;


public class GrabFitug {

	//---------------------------------------------------------------	
	
	private String basePath = "/home/hernani/uzh/FS2012/wahatttt/fitug_xml/";
	private int startYear = 96;
	private int startMonth = 6;
	
	//---------------------------------------------------------------	

	public static void main (String[] argl) {
		try {
			new GrabFitug().scanAll ();
		} catch (Exception e) {
			e.printStackTrace();
		}
	}

	//---------------------------------------------------------------	

	private void scanAll () throws Exception {

		String date;
		int year = startYear;
		int month = startMonth;
		
		boolean busy = true;
		do {
			// calculate the date.
			date = (year  < 10 ? "0" : "") + year +
				   (month < 10 ? "0" : "") + month;
				   
			// process the list.
			busy = processThreadList (date);
			
			// get next date.
			if (++month == 13) {
				month = 1;
				if (++year == 100)
					year = 0;
			}		
		} while (busy);		
	}

	//---------------------------------------------------------------
	
	private String createXmlEntities(String inStr) {
		String retStr = inStr.replaceAll("\u0018", "").replaceAll("\f", ""). // Ctrl chars
		replaceAll("<","&lt;").replaceAll(">", "&gt;"). 
		replaceAll("&uuml;","ü").replaceAll("&auml;","ä").replaceAll("&ouml;", "ö").
		replaceAll("&Uuml;","Ü").replaceAll("&Auml;","Ä").replaceAll("&Ouml;", "Ö").
		replaceAll("&szlig;","ß").
		replaceAll("&nbsp;","").
		replaceAll("&lt&","&lt;&"). // One special case
		replaceAll("&([a-z]+)=","&amp;$1="); // To replace stuff like "&mode=" in URLs
		return retStr;
	}
	
	//---------------------------------------------------------------

	private boolean processThreadList (String date) {
		
		// generate the threadlist URL
		String baseURL = "http://www.fitug.de/debate/";
		String fileName = "/threads.html";
		String fileURL = baseURL + date + fileName;

		// keep the reply hierarchy
		String[] replyList = new String [30];
		String[] idList    = new String [30];
		int depth = -1;
		
		System.out.println ("processing thread list for " + date);
		String line = "";
		int mailCount = 0;
		try {
			// get the HTML document.
			URL url = new URL (fileURL);
			URLConnection connect = url.openConnection();
			BufferedReader rdr =
				new BufferedReader (
					new InputStreamReader (connect.getInputStream())
				);
			
			// parse content.
			int state = 1;
			while ((line = rdr.readLine()) != null && state > 0) {
				
				// running a state machine.
				switch (state) {
					
					// waiting for start of list.
					case 1:
						if (line.startsWith ("<HR>"))
							state = 2;
						break;
			
					// list processing
					case 2:
						if (line.startsWith ("<LI>")) {
							mailCount++;
							
							if (line.indexOf("follow-up") > -1)
								break;
							else if (line.indexOf ("not available") > -1) {
								if (line.endsWith ("<UL>"))
									depth++;
								break;
							}			
							
							// extract HTML file name.
							String htmlSrc = line.substring (34,47);
							
							// extract user name
							String userName = rdr.readLine();
							boolean isParent = !userName.endsWith ("</LI>");
							userName = userName.substring (
								4, userName.length() - (isParent ? 5 : 10)
							);
							// this is a possible parent, so add it to the list.							
							replyList[depth] = htmlSrc;
								
							// check for wau:
							String lwrName = userName.toLowerCase();
							if (lwrName.indexOf ("wau@") > -1 ||
								 lwrName.indexOf ("wau holland") > -1) {
								 	
								 // process all messages in the tree.
								 for (int i = 0; i < depth+1; i++) {
								 	String parent = (i > 0 ? idList[i-1] : null);
									String origURL = baseURL + date + "/" + replyList[i];
								 	idList[i] = processMessage (origURL, parent);
								 }
							}
						}
						else if (line.startsWith ("<UL>"))
							depth++;
						else if (line.startsWith ("</UL>"))
							depth--;
						break;
				}
			}
		} catch (Exception exc) {
			System.out.println ("# " + line);
			exc.printStackTrace();
			return false;
		}
		return (mailCount > 0);
	}
	
	//---------------------------------------------------------------	

	private String processMessage (String origURL, String parent) {

		String line = "", tmpStr;
		FileOutputStream os = null;
		String msgId = "";
		String fileName = "";
		
		try {
			// get the HTML mail.
			URL url = new URL (origURL);
			URLConnection connect = url.openConnection();
			BufferedReader rdr =
				new BufferedReader (
					new InputStreamReader (connect.getInputStream(),"ISO-8859-1")
				);
			
			// allocate content storage
			StringBuffer content = new StringBuffer ();
			String title = "";
			String author = "";
			String email = "";
			String encoding = "";
			Date date = null;
					
			// parse content.
			System.out.println ("processing mail entry " + origURL);
			int state = 1;
			while ((line = rdr.readLine()) != null && state > 0) {
				
				// System.out.println (line);
				
				// running a state machine.
				switch (state) {
					
					// parse attributes.
					case 1:
						if (line.startsWith ("<!--X-Subject: "))
							title = line.substring (15, line.length()-4);
						
						else if (line.startsWith ("<!--X-From: ")) {
							tmpStr = line.substring (12, line.length()-4);
							author = Converter.getNameFromID (tmpStr);
							email = Converter.getEmailFromID (tmpStr);
						}
						else if (line.startsWith ("<!--X-Date:  ")) {
							tmpStr = line.substring (13, line.length()-10);
							date = Converter.getDateFromString (tmpStr);
						}
						else if (line.startsWith ("<!--X-Message-Id: ")) {
							msgId = line.substring (18, line.length()-4);
							fileName = basePath + Converter.urlEncoded(msgId) + ".xml";
						}
						else if (line.startsWith ("<!--X-Content-Type: ")) {
							encoding = line.substring(20, line.length()-4);
						}
						else if (line.startsWith ("<!--X-Body-of-Message-->")) {
							
							// emit header.
							content.append ("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n");
							content.append ("<document ");
							content.append ("xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" ");
							content.append ("xsi:noNamespaceSchemaLocation=\"../Document.xsd\">\n\n");

							// start document.
							content.append ("  <mail id=\"");
							content.append (Converter.urlDecoded(msgId));
							if (encoding.length() > 0) {
								content.append ("\" encoding=\"");
								content.append (encoding);
							}
							content.append ("\">\n");
							content.append ("    <url>");
							content.append (origURL);
							content.append ("</url>\n");
							content.append ("    <subj>");
							content.append (createXmlEntities(title));
							content.append ("</subj>\n");
							content.append ("    <author>");
							content.append (author);
							content.append("</author>\n");
							content.append ("    <email>");
							content.append (email);
							content.append ("</email>\n");
							content.append ("    <date>");
							content.append (Converter.getStringFromDate (date));
							content.append ("</date>\n");							
							if (parent != null) {
								content.append ("    <references>\n");
								content.append ("      <inReplyTo id=\"");
								content.append (Converter.urlDecoded(parent));
								content.append ("\" />\n");
								content.append ("    </references>\n");							
							}
							content.append ("  </mail>\n\n");
							
							// start extracting the content
							content.append ("  <content>\n");
							state = 2;
						}			
						else if (line.startsWith ("<!--X")) {
							//System.out.println (line);
						}
						break;
						
					// extract the content.
					case 2:
						if (line.startsWith ("<!--X-Body-of-Message-End-->")) {
							content.append ("  </content>\n");
							content.append ("</document>\n");
							state = 0;
							break;
						}
						// transfer content.
						content.append (createXmlEntities(line));
						content.append ("\n");
						break;
				}
			}
			
			// prepare the output.
			if (fileName.length() > 0) {
				System.out.println ("            into file " + fileName);
				os = new FileOutputStream (fileName);
				PrintStream prt = new PrintStream (os);
				prt.print(content.toString());
			} else
				System.out.println ("<skipped>");
			
		} catch (Exception exc) {
			System.out.println ("# " + line);
			exc.printStackTrace();
			return null;
		} finally {
			if (os != null) try { os.close(); } catch (Exception exc) { exc.printStackTrace(); }
		}
		// return document id
		return msgId;
	}
}
