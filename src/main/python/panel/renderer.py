import imgui
import typing
if typing.TYPE_CHECKING:
    import proxy
import json

current_user_data = None
user_id = ""
huanxin_user_id = ""
last_matched_user_id = None
matched_user_data = None

def render(addon):
    global current_user_data
    global user_id
    global huanxin_user_id
    global last_matched_user_id
    global matched_user_data
    addon: proxy.LitmatchAddon = addon
    imgui.begin("Session Info")
    imgui.text("Session ID: " + str(addon.sessionId))
    imgui.text("App Info: " + str(addon.applicationInfo))
    imgui.text("Device ID: " + str(addon.uuid))
    if addon.sessionId is None:
        imgui.end()
        return
    
    _, changed_huanxin_user_id = imgui.input_text("User ID (Huanxin)", huanxin_user_id)
    huanxin_user_id = changed_huanxin_user_id
    if imgui.button("Query Huanxin"):
        current_user_data = addon.info_by_huanxin(huanxin_user_id)
        print(json.dumps(current_user_data, indent=2, ensure_ascii=False))
    
    _, changed_user_id = imgui.input_text("User ID (Internal)", user_id)
    user_id = changed_user_id
    if imgui.button("Query Internal"):
        current_user_data = addon.info(user_id)
        print(json.dumps(current_user_data, indent=2, ensure_ascii=False))
        


    imgui.end()

    if current_user_data is not None:
        imgui.begin("User Data")
        text = json.dumps(current_user_data, indent=2, ensure_ascii=False)
        for line in text.splitlines():
            imgui.text(line)
        imgui.end()
    
    if addon.last_match_user is not None:
        if last_matched_user_id != addon.last_match_user:
            last_matched_user_id = addon.last_match_user
            matched_user_data = addon.info_by_huanxin(last_matched_user_id)
            print(json.dumps(matched_user_data, indent=2, ensure_ascii=False))
        imgui.begin("Matched User Data")
        text = json.dumps(matched_user_data, indent=2, ensure_ascii=False)
        for line in text.splitlines():
            imgui.text(line)
        imgui.end()
        