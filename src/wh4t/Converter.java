/**
 * @author Bernd Fix <bernd@wauland.de>, 2000-2012
 */

package wh4t;

import java.net.URLDecoder;
import java.net.URLEncoder;
import java.sql.Date;
import java.text.SimpleDateFormat;
import java.text.ParsePosition;
import java.util.*;


public class Converter {

	//-----------------------------------------------------------------------	

	public static class ConverterCal extends GregorianCalendar {
		private static final long serialVersionUID = -1333159831319961204L;

		public long getMillis() { return time; }
	}

	//-----------------------------------------------------------------------	

	public static String getNameFromID (String s) {
		int idx = s.indexOf ("<");
		if (idx > 0)
			return s.substring (0, idx-1);
		idx = s.indexOf ("(");
		int last = s.indexOf (")");
		if (idx > -1)
			return s.substring (idx+1, last);
		return s;
	}

	//---------------------------------------------------------------	

	public static String getEmailFromID (String s) {
		int idx = s.indexOf ("<");
		if (idx > -1)
			return s.substring (idx+1, s.length()-1);
		idx = s.indexOf ("(");
		if (idx > 0)
			return s.substring (0, idx-1);
		return s;
	}

	//-----------------------------------------------------------------------	

	public static Date getDateFromString (String s) {
		
		String[] formats = new String[] {
			"EEE, dd MMM yyyy hh:mm:ss",
			"yyyy/MM/dd"
		};
		
		java.util.Date tmpDate = null;
		try {
			int numFormats = formats.length;
			for (int i = 0; i < numFormats; i++) {
				SimpleDateFormat df = new SimpleDateFormat (formats[i], 
															Locale.US);
				ParsePosition pos = new ParsePosition(0);
				df.setLenient (true);
				tmpDate = df.parse (s, pos);
				if (tmpDate != null)
					break;
			}
		} catch (Exception exc) {
			System.out.println ("# " + s);
			exc.printStackTrace();
			tmpDate = null;
		}
		if (tmpDate == null)
			tmpDate = new java.util.Date();
		ConverterCal cal = new ConverterCal();
		cal.setTime (tmpDate);
		return new Date (cal.getMillis());
	}
	
	//-----------------------------------------------------------------------	

	public static String getStringFromDate (Date d) {
		
		SimpleDateFormat df = 
			new SimpleDateFormat ("EEE, dd MMM yyyy hh:mm:ss", Locale.US);
		return df.format (d);
	}
	
	//-----------------------------------------------------------------------	
	
	private static final String forbidden = "*\"\\/?:<>+";
	private static final String[] subst = new String[] {
			"%2A", "%22", "%5C", "%2F", "%3F", "%3A", "%3C", "%3E", "%2B"
	};

	//-----------------------------------------------------------------------	

	public static String urlEncoded (String s) {
		try {
			String result = URLEncoder.encode (s, "UTF-8");
			int numChars = forbidden.length();
			for (int i = 0; i < numChars; i++) {
				int idx;
				while ((idx = result.indexOf (forbidden.charAt(i))) > -1)
					result = result.substring (0, idx) + subst[i] + 
							 result.substring (idx+1);
			}
			return result;
		}
		catch (Exception e) {
			e.printStackTrace();
			return null;
		}
	}
	
	//-----------------------------------------------------------------------	

	public static String urlDecoded (String s) {
		int numSubsts = forbidden.length();
		String result = s;
		for (int i = 0; i < numSubsts; i++) {
			int idx;
			while ((idx = result.indexOf (subst[i])) > -1)
				result = result.substring (0, idx) + forbidden.charAt(i) + 
						 result.substring (idx+3);
		}
		try {
			return URLDecoder.decode (result, "UTF-8");
		}
		catch (Exception e) {
			e.printStackTrace();
			return null;
		}
	}
}

