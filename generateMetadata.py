from src.info import (CompanyName, 
                  AppName, 
                  AppVersion, 
                  OriginalFilename, 
                  FileDescription, 
                  LegalCopyright)


def generate_md(output_path):
    version_content = f"""
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=({AppVersion.replace('.', ',')}),
    mask=0x3f,
    flags=0x0,
    OS=0x4, 
    fileType=0x1, 
    subtype=0x0,
    date=(0, 0) 
    ),
  kids=[ 
    StringFileInfo( 
      [ 
      StringTable(
        u'040904b0',
        [StringStruct(u'CompanyName', u'{CompanyName}'),
        StringStruct(u'ProductName', u'{AppName}'),
        StringStruct(u'ProductVersion', u'{AppVersion}'),
        StringStruct(u'OriginalFilename', u'{OriginalFilename}'),
        StringStruct(u'FileDescription', u'{FileDescription}'),
        StringStruct(u'LegalCopyright', u'{LegalCopyright}'),])
      ]),
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)
"""
    with open(output_path, 'w', encoding='utf-8') as output_file:
        output_file.write(version_content.strip())


if __name__ == "__main__":
    generate_md('metadata.txt')
