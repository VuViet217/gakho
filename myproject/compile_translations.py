"""
Script to compile .po files to .mo files without gettext
"""
import os
import struct
import array

def generate_mo_file(po_file, mo_file):
    """Compile .po file to .mo file using proper gettext format"""
    
    # Parse .po file
    translations = {}
    current_msgid = None
    current_msgstr = None
    in_msgid = False
    in_msgstr = False
    
    with open(po_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.rstrip('\n')
            
            if line.startswith('msgid "'):
                if current_msgid is not None and current_msgstr is not None:
                    translations[current_msgid] = current_msgstr
                current_msgid = line[7:-1]
                current_msgstr = None
                in_msgid = True
                in_msgstr = False
                
            elif line.startswith('msgstr "'):
                current_msgstr = line[8:-1]
                in_msgid = False
                in_msgstr = True
                
            elif line.startswith('"') and line.endswith('"'):
                content = line[1:-1]
                if in_msgstr:
                    current_msgstr += content
                elif in_msgid:
                    current_msgid += content
            else:
                in_msgid = False
                in_msgstr = False
    
    # Add last translation
    if current_msgid is not None and current_msgstr is not None:
        translations[current_msgid] = current_msgstr
    
    # Create proper .mo file with metadata
    HEADER = ''
    keys = [k for k in sorted(translations.keys()) if k]
    
    # Add metadata header (use real newline, not escaped)
    metadata = {
        '': 'Content-Type: text/plain; charset=UTF-8\n'
    }
    
    # Build strings
    offsets = []
    ids = b''
    strs = b''
    
    # First add metadata
    msgid = b''
    msgstr = metadata[''].encode('utf-8')
    offsets.append((len(ids), len(msgid), len(strs), len(msgstr)))
    ids += msgid + b'\x00'
    strs += msgstr + b'\x00'
    
    # Then add translations
    for key in keys:
        msgid = key.encode('utf-8')
        msgstr = translations[key].encode('utf-8')
        
        offsets.append((len(ids), len(msgid), len(strs), len(msgstr)))
        ids += msgid + b'\x00'
        strs += msgstr + b'\x00'
    
    # Calculate offsets
    keystart = 7 * 4 + 16 * len(offsets)
    valuestart = keystart + len(ids)
    
    # Build header
    output = struct.pack('Iiiiiii',
                        0x950412de,           # Magic number
                        0,                    # Version
                        len(offsets),         # Number of entries
                        7 * 4,               # Start of key index
                        7 * 4 + 8 * len(offsets),  # Start of value index
                        0, 0)                # Size and offset of hash table
    
    # Add key index
    for o1, l1, o2, l2 in offsets:
        output += struct.pack('ii', l1, o1 + keystart)
    
    # Add value index
    for o1, l1, o2, l2 in offsets:
        output += struct.pack('ii', l2, o2 + valuestart)
    
    # Add strings
    output += ids + strs
    
    # Write file
    with open(mo_file, 'wb') as f:
        f.write(output)
    
    print(f"Compiled: {po_file} -> {mo_file} ({len(keys)} translations)")

# Compile all .po files
locale_dir = os.path.join(os.path.dirname(__file__), 'locale')

for lang in ['en', 'vi']:
    po_path = os.path.join(locale_dir, lang, 'LC_MESSAGES', 'django.po')
    mo_path = os.path.join(locale_dir, lang, 'LC_MESSAGES', 'django.mo')
    
    if os.path.exists(po_path):
        generate_mo_file(po_path, mo_path)
    else:
        print(f"Not found: {po_path}")

print("\nTranslation compilation completed!")
