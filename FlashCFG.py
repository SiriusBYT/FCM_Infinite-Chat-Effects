from Flashcord_API_Client import * 
import json 

"""
This tool lets you quickly configure your page in a hurry.
Read https://github.com/SiriusBYT/Flashcord/wiki/The-Flashcord-Store-Template for how this file works.

WARNING: If you are quickly generating a page from a Replugged Addon's manifest JSON,
Make SURE to first run "ManifestHooker.py" and then manually verify the information inside the generated "FlashCFG_ManifestHooker.json" file.
Then you can rename the generated JSON file to simply "FlashCFG.json" and THEN you can ultimately finally run this script.
"""

# Edit the following things
AllowAPI = True # Allows the script to connect to the SGN servers in order to make your store page more complete without user input

with open("FlashCFG.json", "r", encoding="utf-8") as FlashCFG:
    FlashCFG_JSON = json.load(FlashCFG)
    Name = FlashCFG_JSON["name"]
    Long_Description = FlashCFG_JSON["long_description"]
    Short_Description = FlashCFG_JSON["short_description"]
    Version = FlashCFG_JSON["version"]
    GitHub_Profile = FlashCFG_JSON["author"]
    GitHub_Contributors = FlashCFG_JSON["contributors"]
    GitHub_Repo = FlashCFG_JSON["github_repo"]
    Store_Embed_FileName = FlashCFG_JSON["img_store"]
    Embed_FileName = FlashCFG_JSON["img_embed"]
    License = FlashCFG_JSON["license"]
    License_Year = FlashCFG_JSON["license_year"]

    isRepluggedPlugin = FlashCFG_JSON["is_rpplugin"]
    isFlashcordCompetitor = FlashCFG_JSON["is_rptheme"]
    areIMGsFullLinks = FlashCFG_JSON["images_are_full_links"]

    Folder_Name = f"{FlashCFG_JSON["internal_name"]}-files"
    Store_Page_Name = f"{FlashCFG_JSON["internal_name"]}.html"
    Discord = FlashCFG_JSON["discord_link"]
    SNDL_Theme = FlashCFG_JSON["sndl_theme"]
    Embed_Color = FlashCFG_JSON["embed_color"]

    GitHub_RepoID = GitHub_Repo.split("/")
    GitHub_RepoID = GitHub_RepoID[-1]

    #print(f"DATA LOADED: {Name} \n{Long_Description}\n {Short_Description} {Version} {GitHub_Profile} {GitHub_Contributors} {GitHub_Repo} {Store_Embed_FileName} {Embed_FileName} {License} {License_Year} {isRepluggedPlugin} {isFlashcordCompetitor} {areIMGsFullLinks} {Folder_Name} {Store_Page_Name} {Discord} {SNDL_Theme} {Embed_Color}")



# NOT recommended to modify, do this only if you know what you're doing! 
if isRepluggedPlugin == True: StoreTemplate = "flashcord/store/templates/default/default-plugin_template.html"
elif isFlashcordCompetitor == True: StoreTemplate = "flashcord/store/templates/default/default-theme_template.html"
else: StoreTemplate = "flashcord/store/templates/default/default-module_template.html"

if areIMGsFullLinks == False:
    Store_Banner = f"{Folder_Name}/{Store_Embed_FileName}"

EmbedTemplate = "flashcord/store/templates/default/default-embed_template.html"
# Don't touch this, it will get overwritten anyways but still. Don't touch just in case.
HTMLFile = ""
# Don't touch this either. This will cause problems if your store page is for a Flashcord Module!
UserFolderName = GitHub_Profile.lower()

def GetEmbedCode():
    HTMLCode = ''
    API_Folders = []
    def CallAPI():
        if isRepluggedPlugin == True: API_Request = "GET/" + "PLUGINS/" + GitHub_Profile.upper()
        elif isFlashcordCompetitor == True: API_Request = "GET/" + "THEMES/" + GitHub_Profile.upper()
        else: API_Request = "GET/" + "MODULES/" + GitHub_Profile.upper()
        RequestResults = Flashcord_API_Client(API_Request)
        return RequestResults
    API_Folders = CallAPI()
    #print("TYPE:",type(API_Folders))
    #print("DATA:",API_Folders)
    if API_Folders != None:
        API_Folders = API_Folders.replace("[","").replace("]","").replace('"','').replace("'","").replace(' ','').split(",")
        for cycle in range (len(API_Folders)):
            API_Folders[cycle] = API_Folders[cycle] + "-files"
        if Folder_Name in API_Folders:
            API_Folders.remove(Folder_Name)
        for cycle in range (len(API_Folders)):
            HTMLCode = HTMLCode + f'<iframe class="Flashcord-Module_Embed" src="{API_Folders[cycle]}/embed.html"></iframe>\n'
    else:
        HTMLCode = HTMLCode + f'<iframe class="Flashcord-Module_Embed" src="{Folder_Name}/embed.html"></iframe>\n'
    return HTMLCode

# This code is disgusting but it works, will optimize when I feel like it.
# NOTICE: this has ZERO error handling (or very little)! This is fucking horrible but I don't know yet how to do those and at the time of writing it's fucking 23h28
def GetHTMLFile(FileConcerned):
    if FileConcerned == "Store Page":
        if isRepluggedPlugin == True:
            File = "flashcord/store/plugins/" + GitHub_Profile.lower() + "/" + Store_Page_Name
        else:
            File = "flashcord/store/modules/" + GitHub_Profile.lower() + "/" + Store_Page_Name
    elif FileConcerned == "Embed":
        if isRepluggedPlugin == True:
            File = "flashcord/store/plugins/" + GitHub_Profile.lower() + "/" + Folder_Name + "/embed.html"
        else:
            File = "flashcord/store/modules/" + GitHub_Profile.lower() + "/" + Folder_Name + "/embed.html"
    else:
        print('[FlashCFG // GetHTMLFile] ERROR: Sirius A was here and pissed on the moon. (What the fuck is a "', FileConcerned, '"?!)')
        return "FUCK"
    return File

def FileBackup(FileToBackup):
    print("[FlashCFG // Backup] The", FileToBackup, "will now be backed up...")
    HTMLFile = GetHTMLFile(FileToBackup)
    HTMLFile_Backup = HTMLFile.replace(".html",".bak-html")
    try:
        with open(HTMLFile, 'r', encoding='utf-8') as HTMLFile_File:
            with open(HTMLFile_Backup, 'w', encoding='utf-8') as HTMLFile_Backup_File:
                HTMLFile_Backup_File.write((HTMLFile_File.read()))
        print("[FlashCFG // Backup] ", HTMLFile_Backup, "has been created and is now backed up.")
    except:
        print("[FlashCFG // Backup] ", HTMLFile_Backup, "doesn't exist! Creating empty file instead...")
        with open(HTMLFile, 'w', encoding='utf-8') as EditHTML_File:
            EditHTML_File.write("")

def HTMLConfigurator(Step):
    # We're doing this the MarkSNDL way, I can't fucking figure out how to do this the objectively better way
    # This is surprisingly way better than the current version of MarkSNDL though LMFAO
    HTMLArray = []
    if Step == 0:
        print("[FlashCFG // HTML-CFG] Now building the Store Page...")
        HTMLFile = GetHTMLFile("Store Page")
        StepFile = "// Store Page"
    elif Step == 1:
        print("[FlashCFG // HTML-CFG] Now building the Embed...")
        HTMLFile = GetHTMLFile("Embed")
        StepFile = "// Embed"
    else:
        print("[FlashCFG // HTML-CFG] ERROR: Sirius A was here and replaced Sirius B's Yae wallpaper with a Kirara one.", '(What the fuck is Step "', Step, '"?!)')
        return "FUCK"

    if AllowAPI == True:
        print('[FlashCFG // HTML-CFG] Connecting to SGN servers to fill the "More by" section...')
        MoreByCode = GetEmbedCode() # NOTICE: Will phone to the SGN servers!
        print(f'[FlashCFG // HTML-CFG] The "More by" section will have:\n{MoreByCode}')
    else:
        MoreByCode = f'<iframe class="Flashcord-Module_Embed" src="{Folder_Name}/embed.html"></iframe>\n'
    

    with open(StoreTemplate, 'r', encoding='utf-8') as StoreTemplate_File:
        with open(EmbedTemplate, 'r', encoding='utf-8') as EmbedTemplate_File:
            with open(HTMLFile, 'w', encoding='utf-8') as EditHTML_File:
                EditHTML_File.write("")
            with open(HTMLFile, 'a', encoding='utf-8') as EditHTML_File:
                if Step == 0:
                    HTMLArray = StoreTemplate_File.readlines()
                elif Step == 1:
                    HTMLArray = EmbedTemplate_File.readlines()
                else:
                    print("[FlashCFG // HTML-CFG] WARNING: Sirius A was here and caused another Big Bang", '(What the fuck is Step "', Step, '"?!)')
                    print("[FlashCFG // HTML-CFG] Also how in the LIVING FUCK DID YOU TRIGGER THIS ERROR without triggering the previous one?")
                    return "FUCK"

                for line in range (len(HTMLArray)):
                    # print('[FlashCGG] Processing Line"', line, '" which is "', HTMLArray[line], '".')
                    HTMLArray[line] = HTMLArray[line].replace("[NAME]", Name)
                    HTMLArray[line] = HTMLArray[line].replace("[SHORT_DESC]", Short_Description)
                    HTMLArray[line] = HTMLArray[line].replace("[LONG_DESC]", Long_Description)
                    HTMLArray[line] = HTMLArray[line].replace("[VERSION]", Version)
                    HTMLArray[line] = HTMLArray[line].replace("[LICENSE_YEAR]", License_Year)
                    HTMLArray[line] = HTMLArray[line].replace("[LICENSE]", License)
                    HTMLArray[line] = HTMLArray[line].replace("[GITHUB_PROFILE]", GitHub_Profile)
                    HTMLArray[line] = HTMLArray[line].replace("[GITHUB_REPO]", GitHub_Repo)
                    HTMLArray[line] = HTMLArray[line].replace("[GITHUB_REPO-ID]", GitHub_RepoID)
                    HTMLArray[line] = HTMLArray[line].replace("[GITHUB_CONTRIBUTORS]", GitHub_Contributors)
                    HTMLArray[line] = HTMLArray[line].replace("[DISCORD_LINK]", Discord)
                    HTMLArray[line] = HTMLArray[line].replace("[THEME]", SNDL_Theme)
                    HTMLArray[line] = HTMLArray[line].replace("[EMBED_COLOR]", Embed_Color)
                    HTMLArray[line] = HTMLArray[line].replace("../[STORE_PAGE_FILENAME]", f"../{Store_Page_Name}")
                    HTMLArray[line] = HTMLArray[line].replace("[FOLDER_NAME]", Folder_Name)
                    HTMLArray[line] = HTMLArray[line].replace("[EMBED_FILENAME]", Embed_FileName)
                    HTMLArray[line] = HTMLArray[line].replace("[STORE_BANNER]", Store_Banner)
                    HTMLArray[line] = HTMLArray[line].replace("[STORE_USER_FOLDER]", UserFolderName)
                    HTMLArray[line] = HTMLArray[line].replace("[FLASHSTORE_API-EMBEDS]", MoreByCode)
                    EditHTML_File.write(HTMLArray[line])
                    ProcessingProgress = ((line+1)/len(HTMLArray))*100
                    print('[FlashCFG // HTML-CFG] Processed Line', line+1, '/', len(HTMLArray), '(', ProcessingProgress, '%).', StepFile)
                    # print('[FlashCGG] Processed Line is now "', HTMLArray[line], '".')

def FlashcordStoreConfig():
    print("[FlashCFG] Script initiated.")
    FileBackup("Store Page")
    HTMLConfigurator(0)
    FileBackup("Embed")
    HTMLConfigurator(1)
    print("[FlashCFG] Script complete.")
    return

FlashcordStoreConfig()