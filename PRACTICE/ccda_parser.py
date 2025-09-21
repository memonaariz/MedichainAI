# ccda_parser.py
import xml.etree.ElementTree as ET
import os

def parse_ccda_for_display(file_path):
    """Parse CCDA file and return display-friendly information (robust version)"""
    import xml.etree.ElementTree as ET
    import os
    print(f"Attempting to parse CCDA file: {file_path}")
    try:
        if not os.path.exists(file_path):
            return {"error": f"File does not exist: {file_path}", "parsed_successfully": False}

        # Parse XML with namespace awareness
        tree = ET.parse(file_path)
        root = tree.getroot()

        # Extract namespaces
        namespaces = {'hl7': 'urn:hl7-org:v3'}
        # Try to get all namespaces from the root
        if '}' in root.tag:
                ns_uri = root.tag.split('}')[0].strip('{')
                namespaces[''] = ns_uri

        # Patient info extraction
        patient_info = {"name": "Unknown", "dob": "Unknown", "gender": "Unknown"}
        try:
            # Find patientRole
            patient_role = root.find('.//hl7:recordTarget/hl7:patientRole', namespaces)
            if patient_role is not None:
                # Name
                name_element = patient_role.find('.//hl7:patient/hl7:name', namespaces)
                if name_element is not None:
                    given = name_element.findtext('hl7:given', '', namespaces)
                    family = name_element.findtext('hl7:family', '', namespaces)
                    patient_info["name"] = f"{given} {family}".strip() or "Unknown"
                # DOB
                birth_time = patient_role.find('.//hl7:patient/hl7:birthTime', namespaces)
                if birth_time is not None and 'value' in birth_time.attrib:
                    dob_val = birth_time.attrib['value']
                    if len(dob_val) >= 8:
                        patient_info["dob"] = f"{dob_val[:4]}-{dob_val[4:6]}-{dob_val[6:8]}"
                # Gender
                gender_code = patient_role.find('.//hl7:patient/hl7:administrativeGenderCode', namespaces)
                if gender_code is not None and 'code' in gender_code.attrib:
                    code = gender_code.attrib['code']
                    if code == 'M':
                        patient_info["gender"] = "Male"
                    elif code == 'F':
                        patient_info["gender"] = "Female"
                    else:
                        patient_info["gender"] = code
        except Exception as e:
            print(f"Error extracting patient info: {e}")
        
        # Medical data extraction
        medical_data = {
            "conditions": [],
            "medications": [],
            "lab_results": [],
            "vital_signs": []
        }
        
        # Problems/Conditions - Improved extraction
        try:
            for section in root.findall('.//hl7:section', namespaces):
                code_elem = section.find('hl7:code', namespaces)
                if code_elem is not None and code_elem.attrib.get('code') == '11450-4':
                    # Try to extract from text content first
                    text_elem = section.find('hl7:text', namespaces)
                    if text_elem is not None:
                        # Look for list items in text
                        for item in text_elem.findall('.//hl7:item', namespaces):
                            content = item.find('hl7:content', namespaces)
                            if content is not None and content.text:
                                medical_data["conditions"].append(content.text.strip())
                        
                        # Also try to extract from entry relationships
                        for entry in section.findall('hl7:entry', namespaces):
                            act = entry.find('hl7:act', namespaces)
                            if act is not None:
                                entry_rel = act.find('.//hl7:entryRelationship', namespaces)
                                if entry_rel is not None:
                                    obs = entry_rel.find('hl7:observation', namespaces)
                                    if obs is not None:
                                        value = obs.find('hl7:value', namespaces)
                                        if value is not None and 'displayName' in value.attrib:
                                            medical_data["conditions"].append(value.attrib['displayName'])
        except Exception as e:
            print(f"Error extracting conditions: {e}")
        
        # Medications - Improved extraction
        try:
            for section in root.findall('.//hl7:section', namespaces):
                code_elem = section.find('hl7:code', namespaces)
                if code_elem is not None and code_elem.attrib.get('code') == '10160-0':
                    # Try to extract from text content first
                    text_elem = section.find('hl7:text', namespaces)
                    if text_elem is not None:
                        # Look for table content
                        for table in text_elem.findall('.//hl7:table', namespaces):
                            for row in table.findall('.//hl7:tr', namespaces):
                                cells = row.findall('.//hl7:td', namespaces)
                                if len(cells) > 0:
                                    content = cells[0].find('hl7:content', namespaces)
                                    if content is not None and content.text:
                                        medical_data["medications"].append(content.text.strip())
                        
                        # Also try to extract from substance administration
                        for entry in section.findall('hl7:entry', namespaces):
                            substance = entry.find('hl7:substanceAdministration', namespaces)
                            if substance is not None:
                                consumable = substance.find('hl7:consumable', namespaces)
                                if consumable is not None:
                                    manufactured = consumable.find('hl7:manufacturedProduct', namespaces)
                                    if manufactured is not None:
                                        material = manufactured.find('hl7:manufacturedMaterial', namespaces)
                                        if material is not None:
                                            code = material.find('hl7:code', namespaces)
                                            if code is not None and 'displayName' in code.attrib:
                                                medical_data["medications"].append(code.attrib['displayName'])
        except Exception as e:
            print(f"Error extracting medications: {e}")
        
        # Lab Results - Improved extraction
        try:
            for section in root.findall('.//hl7:section', namespaces):
                code_elem = section.find('hl7:code', namespaces)
                if code_elem is not None and code_elem.attrib.get('code') == '30954-2':
                    for entry in section.findall('hl7:entry', namespaces):
                        obs = entry.find('hl7:observation', namespaces)
                        if obs is not None:
                            code = obs.find('hl7:code', namespaces)
                            value = obs.find('hl7:value', namespaces)
                            if code is not None and value is not None:
                                name = code.attrib.get('displayName', 'Lab Test')
                                val = value.attrib.get('value', '')
                                unit = value.attrib.get('unit', '')
                                result = f"{name}: {val} {unit}".strip()
                                medical_data["lab_results"].append(result)
        except Exception as e:
            print(f"Error extracting lab results: {e}")
        
        # Vital Signs - Improved extraction
        try:
            for section in root.findall('.//hl7:section', namespaces):
                code_elem = section.find('hl7:code', namespaces)
                if code_elem is not None and code_elem.attrib.get('code') == '8716-3':
                    for entry in section.findall('hl7:entry', namespaces):
                        obs = entry.find('hl7:observation', namespaces)
                        if obs is not None:
                            code = obs.find('hl7:code', namespaces)
                            value = obs.find('hl7:value', namespaces)
                            if code is not None and value is not None:
                                name = code.attrib.get('displayName', 'Vital')
                                val = value.attrib.get('value', '')
                                unit = value.attrib.get('unit', '')
                                vital = f"{name}: {val} {unit}".strip()
                                medical_data["vital_signs"].append(vital)
        except Exception as e:
            print(f"Error extracting vital signs: {e}")
        
        # Fallback if nothing found
        if not any(medical_data.values()):
                medical_data = {
                    "conditions": ["No conditions found in document"],
                    "medications": ["No medications found in document"],
                    "lab_results": ["No lab results found in document"],
                    "vital_signs": ["No vital signs found in document"]
                }
        
        print(f"DEBUG - Extracted patient: {patient_info}")
        print(f"DEBUG - Extracted medical: {medical_data}")
        
        return {
            "patient": patient_info,
            "medical": medical_data,
            "parsed_successfully": True
        }
    except Exception as e:
        return {"error": f"Failed to parse CCDA: {str(e)}", "parsed_successfully": False}