#*    pyx509 - Python library for parsing X.509
#*    Copyright (C) 2009-2012  CZ.NIC, z.s.p.o. (http://www.nic.cz)
#*
#*    This library is free software; you can redistribute it and/or
#*    modify it under the terms of the GNU Library General Public
#*    License as published by the Free Software Foundation; either
#*    version 2 of the License, or (at your option) any later version.
#*
#*    This library is distributed in the hope that it will be useful,
#*    but WITHOUT ANY WARRANTY; without even the implied warranty of
#*    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#*    Library General Public License for more details.
#*
#*    You should have received a copy of the GNU Library General Public
#*    License along with this library; if not, write to the Free
#*    Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
#*

import sys
from binascii import hexlify

from pkcs7.asn1_models.X509_certificate import Certificate
from pkcs7_models import X509Certificate, PublicKeyInfo, ExtendedKeyUsageExt

from pkcs7.asn1_models.decoder_workarounds import decode
import MySQLdb
import chilkat
def ConnectDB():
    try:
        db = MySQLdb.connect(host="conan.soic.indiana.edu",port=13306,user="PlanetLab",passwd="Informatics",db="certprobe")
        return db
    except Exception, e:
        print ('DB connection Error: %s.' %(`e`))
        return 0


def x509_parse(derData):
	"""Decodes certificate.
	@param derData: DER-encoded certificate string
	@returns: pkcs7_models.X509Certificate
	"""
	cert = decode(derData, asn1Spec=Certificate())[0]
	x509cert = X509Certificate(cert)
	return x509cert

def parse_pem(pemstr):
	dict = {}
	f = open('temp.crt','w')
	f.write(pemstr)
	f.close()
	cert.LoadFromFile('temp.crt')	 
	cert.ExportCertDerFile('temp_der.der')
	f = open('temp_der.der','r')
	cer = f.read()
	f.close()
	x509cert = x509_parse(cer)
	tbs = x509cert.tbsCertificate
    if tbs != None:
        #version
        #attributes_writer.write(str(tbs.version +1) + ',')
	    dict["version"] = tbs.version + 1
        #Serial no
        #attributes_writer.write(str(tbs.serial_number) + ',')
        dict["Serial No"] = hex(tbs.serial_number)    
   	 	#Signatue algorithm
        #attributes_writer.write(x509cert.signature_algorithm + ',')
        dict['Sig Alg'] = x509cert.signature_algorithm    
	    #Issuer
	    temp = tbs.issuer.get_attributes()
        temp_dict = {}

	    if 'CN' in temp.keys():
	        value = temp.get('CN')[0]
	    else:
			value = ''
	    
	    temp_dict['CN'] = value

	    if 'C' in temp.keys():
            	value = temp.get('C')[0]
	    else:
			value = ''
	    
	    temp_dict['C'] = value

	    if 'L' in temp.keys():
			value = temp.get('L')[0]
	    else:
			value = ''
	    
	    temp_dict['L'] = value
		
	    if 'ST' in temp.keys():
			value = temp.get('ST')[0]
	    else:
	        value = ''
	    
	    temp_dict['ST'] = value

	    if 'O' in temp.keys():
			value = temp.get('O')[0]
	    else:
			value = ''
	    
	    temp_dict['O'] = value
	    	
	    if 'OU' in temp.keys():
			value = temp.get('OU')[0]
	    else:
			value = ''
	    
	    temp_dict['OU'] = value
	    
	    dict['issuer'] = temp_dict
            		
	    #Not Before Not After

	    #attributes_writer.write(str(tbs.validity.get_valid_from_as_datetime()) +',')
	    #attributes_writer.write(str(tbs.validity.get_valid_to_as_datetime()) + ',')
            #print tbs.validity.get_valid_from_as_datetime()
	    dict['Not Before'] = tbs.validity.get_valid_from_as_datetime()
	    dict['Not After'] = tbs.validity.get_valid_to_as_datetime()
	    
	    #Subject
	    temp = tbs.subject.get_attributes()
	    temp_dict = {}
	    if 'CN' in temp.keys():
			value = temp.get('CN')[0]
	    else:
			value = ''
	    
        temp_dict['CN'] = value	    

	    if 'C' in temp.keys():
            value = temp.get('C')[0]
	    else:
			value = ''
	    
	    temp_dict['C'] = value
	
	    if 'L' in temp.keys():
	        value = temp.get('L')[0]
	    else:
			value = ''
	    
	    temp_dict['L'] = value
	
	    if 'ST' in temp.keys():
			value = temp.get('ST')[0]
	    else:
			value = ''
	    
	    temp_dict['ST'] = value
		
	    if 'O' in temp.keys():
			value = temp.get('O')[0]
	    else:
			value = ''
	    
	    temp_dict['O'] = value	
	    if 'OU' in temp.keys():
			value = temp.get('OU')[0]
	    else:
			value = ''
	    
	    temp_dict['OU'] = value	
 	    dict['Subject'] = temp_dict
	    #public key algorithm && type
	    #attributes_writer.write(str(tbs.pub_key_info.algName) + ',')
	    alg = ''
	    temp_dict = {}
	    algParams = tbs.pub_key_info.key
	    if tbs.pub_key_info.algType == PublicKeyInfo.RSA:
	        #attributes_writer.write('RSA' + ',')
			temp_dict['pKeyType'] = 'RSA'
			temp_dict['Modulus'] = hexlify(algParams["mod"])
			temp_dict['Exponent'] = hex(algParams["exp"])
	    elif tbs.pub_key_info.algType == PublicKeyInfo.DSA:
			#attributes_writer.write('DES' + ',')
		   	temp_dict['pKeyType'] = 'DES'
			temp_dict['Pub'] = hexlify(algParams['pub'])
			temp_dict['P'] = hexlify(algParams['p'])
	 		temp_dict['Q'] = hexlify(algParams['q'])
			temp_dict['G'] = hexlify(algParams['g'])
	    dict['pKeyAlg'] = temp_dict
	    
	    temp_dict = {}
	    #Extensions
	    if tbs.authInfoAccessExt:
	        #attributes_writer.write(str(tbs.authInfoAccessExt.is_critical))
			son_dict = {}
			son_dict['is_critical'] = tbs.authInfoAccessExt.is_critical
			temp = '['
			for aia in tbs.authInfoAccessExt.value:
			    temp +='{' +  aia.access_location + ',' + aia.access_method + ',' + str(aia.id) + '},'
			temp += ']'    
			son_dict['value'] = temp
			temp_dict['authInfoAccessExt'] = son_dict	
		#attributes_writer.write(loc + ',' + acm + ',' + id + ',')
	

	    if tbs.authKeyIdExt:
	        aki = tbs.authKeyIdExt.value
			kd = ''
	  		acs = ''
			aci = ''
			if hasattr(aki, "key_id"):
			    kd = str(hexlify(aki.key_id))
			if hasattr(aki, "auth_cert_sn"):
			    acs = aki.auth_cert_sn
			if hasattr(aki, "auth_cert_issuer"):
			    aci = aki.auth_cert_issuer
			son_dict = {}
			son_dict['is_critical'] = tbs.authKeyIdExt.is_critical
			son_dict['value'] = '{' + kd + ',' + acs +',' +aci + '}'
			temp_dict['authKeyIdExt'] = son_dict

	    if tbs.basicConstraintsExt:
			bc = tbs.basicConstraintsExt.value
			son_dict = {}
			son_dict['is_critical'] = tbs.basicConstraintsExt.is_critical
			son_dict['value'] = '{' + str(bc.ca) + ',' + str(bc.max_path_len) + '}'
			temp_dict['basicConstraintsExt'] = son_dict
 		
		
	    if tbs.certPoliciesExt:
	        son_dict = {}
			policies = tbs.certPoliciesExt.value
			son_dict['is_critical'] = tbs.certPoliciesExt.is_critical
			temp = ''
			for policy in policies:
			    temp += '['+str(policy.id)
			    for qualifier in policy.qualifiers:
			        temp += '{' + str(qualifier.id) + ',' +str(qualifier.qualifier) + '}'
		    	temp += '],'
			son_dict['value'] = temp
			temp_dict['certPoliciesExt'] = son_dict


	    if tbs.crlDistPointsExt:
	        son_dict = {}
			son_dict['is_critical'] = tbs.crlDistPointsExt.is_critical
			crls = tbs.crlDistPointsExt.value
			temp = '['
			for crl in crls:
			    if crl.dist_point:
			        temp += '{' + crl.dist_point + ','
			    else:
					temp += '{' + ','
			    if crl.issuer:
			        temp += crl.issuer + ','
			    else:
					temp += ','
			    if crl.reasons:
					temp += crl.reasons + '},'
			    else:
					temp += '},'
			temp += ']'
			son_dict['value'] = temp
			temp_dict['crlDistPointsExt'] = son_dict

	    if tbs.extKeyUsageExt:
			eku = tbs.extKeyUsageExt.value
			set_flags = [flag for flag in ExtendedKeyUsageExt._keyPurposeAttrs.values() if getattr(eku, flag)]
			son_dict = {}
			son_dict['is_critical'] = tbs.extKeyUsageExt.is_critical
			son_dict['value'] = set_flags
			temp_dict['extKeyUsageExt'] = son_dict

	
	    if tbs.keyUsageExt:
		    #print "\tKey Usage: is_critical:", tbs.keyUsageExt.is_critical
			ku = tbs.keyUsageExt.value
			flags = ["digitalSignature","nonRepudiation", "keyEncipherment",
				 "dataEncipherment", "keyAgreement", "keyCertSign",
				 "cRLSign", "encipherOnly", "decipherOnly",
				]

			set_flags = [flag for flag in flags if getattr(ku, flag)]
			    #print "\t\t", ",".join(set_flags)
			son_dict = {}
			son_dict['is_critical'] = tbs.keyUsageExt.is_critical
			son_dict['value'] = set_flags
			temp_dict['KeyUsageExt'] = son_dict
		
	    if tbs.policyConstraintsExt:
		    #print "\tPolicy Constraints: is_critical:", tbs.policyConstraintsExt.is_critical
	    	pc = tbs.policyConstraintsExt.value
		   # print "\t\trequire explicit policy: ", pc.requireExplicitPolicy
 		   # print "\t\tinhibit policy mapping: ", pc.inhibitPolicyMapping
			son_dict = {}
			son_dict['is_critical'] = tbs.policyConstraintsExt.is_critical
			son_dict['value'] = '{' + pc.requireExplicitPolicy + ',' + pc.inhibitPolicyMapping + '}'
			temp_dict['policyConstraintsExt'] = son_dict

	    if tbs.subjAltNameExt:
		   # print "\tSubject Alternative Name: is_critical:", tbs.subjAltNameExt.is_critical
			san = tbs.subjAltNameExt.value
			   # print "\t\tDNS names:", ",".join(san.names) #only DNS names supported now
			son_dict = {}
			son_dict['is_critical'] = tbs.subjAltNameExt.is_critical
			son_dict['value'] = san.names
			temp_dict['subjAltNameExt'] = son_dict

				
	    if tbs.subjKeyIdExt:
		    #print "\tSubject Key Id: is_critical:", tbs.subjKeyIdExt.is_critical
			ski = tbs.subjKeyIdExt.value
			   # print "\t\tkey id", hexlify(ski.subject_key_id)
			son_dict = {}
			son_dict['is_critical'] = tbs.subjKeyIdExt.is_critical
			son_dict['value'] = ski.subject_key_id
			temp_dict['subjKeyIdExt'] = son_dict

		
	    if tbs.nameConstraintsExt:
			nce = tbs.nameConstraintsExt.value
			   # print "\tName constraints: is_critical:", tbs.nameConstraintsExt.is_critical

			subtreeFmt = lambda subtrees: ", ".join([str(x) for x in subtrees])
			permit = ''
	  		exc = ''
			if nce.permittedSubtrees:
			    permit = subtreeFmt(nce.permittedSubtrees)	
				#print "\t\tPermitted:", subtreeFmt(nce.permittedSubtrees)
			if nce.excludedSubtrees:
			    exc = subtreeFmt(nce.excludedSubtrees)
				#print "\t\tExcluded:", subtreeFmt(nce.excludedSubtrees)
			son_dict = {}
			son_dict['is_critical'] = tbs.nameConstrainsExt.is_critical
			son_dict['value'] = '{'+permit+',' + exc + '}'
			temp_dict['nameConstraintsExt'] = son_dict
	dict['Extension'] = temp_dict
	#signature
	dict['signature'] = hexlify(x509cert.signature)
	print dict
   	return dict

#Sample usage showing retrieving certificate fields
if __name__ == "__main__":
	db =  ConnectDB()
	cursor = db.cursor()
	try:
		query_str = "SELECT pem_str FROM SOIC_certs LIMIT 0,1"
		cursor.execute(query_str)
		row = cursor.fetchone()
		while row is not None:
			parse_pem(row[0])
			row = cursor.fetchone()
		cursor.close()
	except Exception, e:
		print ('SELECT query Error: %s.' %(`e`))
		cursor.close()
		return -1

