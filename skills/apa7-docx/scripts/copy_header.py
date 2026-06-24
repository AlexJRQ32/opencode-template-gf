"""
Copy header (including images) from one DOCX to another via direct ZIP manipulation.
"""
import zipfile
import os
import re
from xml.etree import ElementTree as ET

NS = {
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
    "rel": "http://schemas.openxmlformats.org/package/2006/relationships",
}


def copy_header_with_images(original_path, new_path):
    """
    Copy header XML, header relationships, and header images from original DOCX
    to new DOCX. Works in-memory, writes back to new_path.
    """
    # Read both archives into dicts
    original_entries = _read_zip(original_path)
    new_entries = _read_zip(new_path)

    # Determine header rels in the original
    header_rels_path = "word/_rels/header1.xml.rels"
    header_xml_path = "word/header1.xml"

    if header_xml_path not in original_entries:
        print("INFO: No header1.xml in original, nothing to copy.")
        return

    if header_rels_path not in original_entries:
        print("INFO: No header1.xml.rels in original.")
        # Still copy the header XML itself
        new_entries[header_xml_path] = original_entries[header_xml_path]
    else:
        # Copy header XML and its rels
        new_entries[header_xml_path] = original_entries[header_xml_path]
        new_entries[header_rels_path] = original_entries[header_rels_path]

        # Find which images the header references
        rels_xml = original_entries[header_rels_path].decode("utf-8")
        rel_root = ET.fromstring(rels_xml)
        for rel_elem in rel_root.findall("rel:Relationship", {"rel": NS["rel"]}):
            target = rel_elem.get("Target", "")
            if target.startswith("media/"):
                media_path = f"word/{target}"
                if media_path in original_entries:
                    new_entries[media_path] = original_entries[media_path]
                    print(f"  Copied {media_path}")
                else:
                    print(f"  WARNING: {media_path} not found in original!")

    # Replace Spanish "Encabezado" style with English "Header" style
    header_xml = new_entries[header_xml_path].decode("utf-8")
    header_xml = header_xml.replace('w:val="Encabezado"', 'w:val="Header"')
    new_entries[header_xml_path] = header_xml.encode("utf-8")

    # Ensure document.xml.rels has header relationship
    doc_rels_path = "word/_rels/document.xml.rels"
    if doc_rels_path in new_entries:
        doc_rels_xml = new_entries[doc_rels_path].decode("utf-8")
        if 'Target="header1.xml"' not in doc_rels_xml:
            # Add header relationship
            doc_rels_xml = doc_rels_xml.replace(
                "</Relationships>",
                '<Relationship Id="rIdHeader1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/header" Target="header1.xml"/></Relationships>',
            )
            new_entries[doc_rels_path] = doc_rels_xml.encode("utf-8")
            print("  Added header relationship to document.xml.rels")

    # Ensure document.xml has headerReference
    doc_path = "word/document.xml"
    if doc_path in new_entries:
        doc_xml = new_entries[doc_path].decode("utf-8")
        if "w:headerReference" not in doc_xml:
            # Add headerReference to the first section (last sectPr in document)
            # Find the last closing sectPr tag and insert before it
            # Simple approach: insert right before </w:sectPr>
            # We need to find ALL sectPr elements and target the last one
            # More robust: find all occurrences and work with the last
            parts = doc_xml.rsplit("</w:sectPr>", 1)
            if len(parts) == 2:
                header_ref = (
                    '<w:headerReference w:type="default" r:id="rIdHeader1"/>'
                )
                doc_xml = parts[0] + header_ref + "</w:sectPr>" + parts[1]
                new_entries[doc_path] = doc_xml.encode("utf-8")
                print("  Added headerReference to document.xml")
    else:
        print("  WARNING: word/document.xml not found!")

    # Ensure [Content_Types].xml includes PNG content type
    ct_path = "[Content_Types].xml"
    if ct_path in new_entries:
        ct_xml = new_entries[ct_path].decode("utf-8")
        if '<Default Extension="png" ContentType="image/png"/>' not in ct_xml:
            ct_xml = ct_xml.replace(
                "<Types", '<Types><Default Extension="png" ContentType="image/png"/>', 1
            )
            new_entries[ct_path] = ct_xml.encode("utf-8")
            print("  Added PNG content type to [Content_Types].xml")

    # Write updated archive back to new_path
    _write_zip(new_entries, new_path)
    print(f"OK: Header copied from {original_path} to {new_path}")


def _read_zip(path):
    """Read a ZIP file into {entry_path: bytes} dict."""
    entries = {}
    with zipfile.ZipFile(path, "r") as z:
        for name in z.namelist():
            entries[name] = z.read(name)
    return entries


def _write_zip(entries, path):
    """Write entries dict back to a ZIP file."""
    import tempfile
    tmp = path + ".tmp"
    with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as z:
        for name, data in entries.items():
            z.writestr(name, data)
    os.replace(tmp, path)
