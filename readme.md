# Litatom Reverse Engineer Project

**Author:** fan87 / TropicalFan344

*NOT affiliated or associated with Construct Technology PTE. LTD.*


## I. Introduction
Litatom (Also known as Litmatch) is a networking/social Android app built with Java and
Kotlin. It's a full stack app as it has a fully functional backend (Instead of a simple firebase
database). It has some security features, and we thought it's worth doing research
on Litatom.

The app package name is `com.litatom.app`, in the time of researching, the latest
version is `6.15.0`, the API may differ in future updates.

The app doesn't support x86 devices, you may have to install 
`libhoudini` or use an actual ARM device for this.


### Reversing Environment Setup
> ⚠ This section is only for people who want to reverse the app

It's recommended to use an actual ARM device as Gdb could not debug libraries
loaded with `libhoudini`, although it's not needed, but still recommended.

It's also recommended to have root on the device, you can easily debug apps
without any difficulties.

Our setup is Raspberry Pi 4 with [KonstaKANG's LineageOS Build](https://konstakang.com/devices/rpi4/AOSP13/)
with Gapps and Magisk (Means we have root access). We were originally using `Waydroid`, it will work if you are only gonna be hooking into Java functions using `Frida` or MITM (Man-in-the-middle) HTTP requests.


## II. Requests/Responses
Litatom app starts an OkHttp instance with SSL Pinning (Optional) on start with base
URL of `www.litatom.com` (In `6.15.0`). The SSL pinning is optional because
it could be disabled by changing `remote_config` configuration in Google Play Measurement.

To bypass SSL pinning, you either modify `remote_config` from Google Play Service Measurement (Requires root),
or use `frida` or other tools to hook into the LitNetwork initialization method
(Where it initializes the OkHttp client), and modify the remote config before, which is 
the method we have chosen to use.

The frida script is quiet simple, it does literal what it is.

Note that the mapping may differ on your side, but you find where it initializes
OkHttp Client anyway.

```ts
const LitNetwork = Java.use("b.f0.a.d"); // com.lit.net.LitNetwork
LitNetwork.b.implementation = function( // Init function
    context: any,
    config: any
) {
    console.log("Pre initialize   " + config.g.value)
    config.g.value = false; // config.enable_ssl_pin = true
    this.b(context, config); // this.init(context, config);
    console.log("Post initialize  " + config.g.value)
}
```

### Endpoints
All the endpoints are listed below as the time of writing:

```
"api/sns/v1/lit/cloud_music/get_musics"
"api/sns/v1/lit/last_man_standing/get_game_status"
"api/sns/v1/lit/party/get_token"
"api/sns/v1/lit/broadcast_feed_tickets"
"api/sns/v1/lit/broadcast_feeds"
"api/sns/v1/lit/following_filter_by_age_gap"
"api/sns/v1/lit/broadcast_feeds_translation"
"api/sns/v1/lit/broadcast_feed"
"api/sns/v1/lit/magic_box/grab_resource"
"api/sns/v1/lit/activity/share_settings"
"api/sns/v1/lit/account/reset_rate_by_diamonds"
"api/sns/v1/lit/avatar/confirm_avatar"
"api/sns/v1/lit/avatar/get_products_using"
"api/sns/v1/lit/home/track_network"
"api/sns/v1/lit/home/settings"
"api/sns/v1/lit/home/acted_actions"
"api/sns/v1/lit/effect/change_effects"
"api/sns/v1/lit/frame/frame_shop"
"api/sns/v1/lit/propose/ring_shop"
"api/sns/v1/lit/avatar/get_classify"
"api/sns/v1/lit/home/record_mock"
"api/sns/v1/lit/home/check_version"
"api/ms/v1/profile/cold-start/sync"
"api/sns/v1/lit/effect/effects_shop"
"api/sns/v1/lit/home/im_warn_setting"
"api/sns/v1/lit/home/track_action"
"api/sns/v1/lit/avatar/get_products"
"api/sns/v1/lit/home/report_acted"
"api/sns/v1/lit/avatar/get_own_products"
"api/sns/v1/lit/home/polling_vids"
"api/sns/v1/lit/home/app_pull_region_words"
"api/sns/v1/lit/push/push_callback"
"api/sns/v1/lit/frame/change_frames"
"api/sns/v1/lit/user/get_info/{userId}"
"api/sns/v1/lit/follow/{user}"
"api/sns/v1/lit/user/search_contact"
"api/sns/v1/lit/contact/{type}"
"api/sns/v1/lit/contact/{type}"
"api/sns/v1/lit/contact/{type}"
"api/sns/v1/lit/feed/dislike/{id}"
"api/sns/v1/lit/feed/get_daily_festival_effects"
"api/sns/v1/lit/feed/delete/{id}"
"api/sns/v1/lit/propose/get_love_story"
"api/sns/v1/lit/feed/comment/like/{comment_id}"
"api/sns/v1/lit/feed/got_regulation"
"api/sns/v1/lit/feed/unfollow_tag"
"api/sns/v1/lit/feed/del_comment/{id}"
"api/sns/v1/lit/video/upload"
"api/sns/v1/lit/feed/follow_tag"
"api/sns/v1/lit/feed/view/{user}"
"api/sns/v1/lit/feed/tag_info"
"api/sns/v1/lit/feed/nearby"
"api/sns/v1/lit/feed/repost_feed/{feed_id}"
"api/sns/v1/lit/feed/hq"
"api/sns/v1/lit/feed/comment/{id}"
"api/sns/v1/lit/feed/tags"
"api/sns/v1/lit/feed/vote"
"api/sns/v1/lit/feed/sep_page_feeds/{type}"
"api/sns/v1/lit/feed/location"
"api/sns/v1/lit/feed/pin_feed/{id}"
"api/sns/v1/lit/feed/comment/{id}"
"api/sns/v1/lit/feed/square"
"api/sns/v1/lit/feed/unpin_feed/{id}"
"api/sns/v1/lit/feed/info/{id}"
"api/sns/v1/lit/feed/square"
"api/sns/v1/lit/feed/location_cnt"
"api/sns/v1/lit/feed/following_feeds"
"api/sns/v1/lit/home/init_resources"
"api/sns/v1/lit/feed/comment_page/{id}"
"api/sns/v1/lit/feed/reaction_list/{id}"
"api/sns/v1/lit/anoy_match/video_info_list"
"api/sns/v1/lit/home/feedback"
"api/sns/v1/lit/privacy/setting"
"api/sns/v1/lit/group/report_spam"
"api/sns/v1/lit/url_shorten"
"api/sns/v1/lit/mission/get_user_mission_overview"
"api/sns/v1/lit/party/get_in_party_friends"
"api/sns/v1/lit/vip/set_show_vip_status"
"api/sns/v1/lit/home/report_setting"
"api/sns/v1/lit/ad/times_left"
"api/ms/v1/profile/match/free-match-acceleration"
"api/sns/v1/lit/ad/reset_accost"
"api/sns/v1/lit/anoy_match/quit_match"
"api/sns/v1/lit/home/online_users"
"api/sns/v1/lit/anoy_match/end_match"
"api/sns/v1/lit/privacy/set_accost_gift"
"api/sns/v1/lit/home/video_pic_check"
"api/sns/v1/lit/home/report_setting"
"api/sns/v1/lit/privacy/set_active_status"
"api/sns/v1/lit/account/pay_privacy_setting"
"api/sns/v1/lit/anoy_match/anoy_match"
"api/sns/v1/lit/anoy_match/accelerate_info"
"api/sns/v1/lit/user_tag/get_same_tags"
"api/sns/v1/lit/anoy_match/anoy_like"
"api/sns/v1/lit/anoy_match/add_time_by_ad"
"api/sns/v1/lit/privacy/get_accost_gifts"
"api/sns/v1/lit/anoy_match/get_fakeid"
"api/sns/v1/lit/anoy_match/judge"
"api/sns/v1/lit/home/spam_words"
"api/sns/v1/lit/home/refresh_nums"
"api/sns/v1/lit/anoy_match/accelerate_by_ad"
"api/sns/v1/lit/home/report_spam"
"api/sns/v1/lit/home/online_users"
"api/ms/v1/profile/match/free-match-acceleration"
"api/sns/v1/lit/home/user_feedback"
"api/sns/v1/lit/anoy_match/times_left"
"api/sns/v1/lit/chat/get_chat_token"
"api/sns/v1/lit/account/send_gift/{user}"
"api/ms/v1/aigc/chatbot"
"api/sns/v1/lit/account/send_gift/{user}"
"api/sns/v1/lit/gift/gift_bag"
"api/sns/v1/lit/user/batch_accost"
"api/sns/v1/lit/user/pin_conversation"
"api/sns/v1/lit/user/crush_card"
"api/sns/v1/lit/lt/batch_chat_level_info"
"api/sns/v1/lit/huanxin/set_im_unread_count"
"api/sns/v1/lit/group/sc"
"api/sns/v1/lit/account/send_gift/{user}"
"api/sns/v1/lit/user/info_by_huanxin"
"api/ms/v1/aigc/chatbot"
"api/sns/v1/lit/lt/sc"
"api/sns/v1/lit/user/sticky_message"
"api/sns/v1/lit/lt/chat_level_count"
"api/sns/v1/lit/user/unpin_conversation"
"api/sns/v1/lit/user/batch_accost_settings"
"api/sns/v1/lit/user/add_customize_emoticons"
"api/sns/v1/lit/user/get_customize_emoticons"
"api/ms/v1/aigc/chatbot/messages/{msg-id}/reaction"
"api/sns/v1/lit/gift/gifts"
"api/sns/v1/lit/user/tiktok_login"
"api/sns/v1/lit/user/google_login"
"api/sns/v1/lit/user/logout"
"api/sns/v1/lit/user/facebook_login"
"api/sns/v1/lit/user/extra_settings"
"api/sns/v1/lit/user/get_info/{userId}"
"api/sns/v1/lit/user/phone_login"
"api/sns/v1/lit/user/get_info/{userId}"
"api/sns/v1/lit/social/userrec"
"api/sns/v1/lit/get_sms_code"
"api/sns/v1/lit/user/search"
"api/sns/v1/lit/user/get_info/{userId}"
"api/sns/v1/lit/user/extra_settings"
"api/sns/v1/lit/user/info"
"api/sns/v1/lit/user/avatars"
"api/sns/v1/lit/account/query_sub_vip"
"api/sns/v1/lit/account/diamonds_for_gift"
"api/sns/v1/lit/account/get_subscribe_vip_conf"
"api/sns/v1/lit/ad/watch_incentive_video"
"api/sns/v1/lit/activity/claim_rewards"
"api/sns/v1/lit/account/buy_product"
"api/sns/v1/lit/account/pay_activities"
"api/sns/v1/lit/account/judge_buy_onetime_product"
"api/sns/v1/lit/account/new_diamonds_product"
"api/sns/v1/lit/account/query_pay_order"
"api/sns/v1/lit/account/report_google_purchase_history"
"api/sns/v1/lit/account/release_order"
"api/sns/v1/lit/account/pay_order"
"api/sns/v1/lit/activity/share_num"
"api/sns/v1/lit/account/products"
"api/sns/v1/lit/account/record_order"
"api/sns/v1/lit/account/diamonds_record"
"api/sns/v1/lit/ad/get_ad_conf"
"api/sns/v1/lit/account/deposit_by_activity"
"api/sns/v1/lit/account/android_subs_status"
"api/sns/v1/lit/account/pay_setting_by_product_id"
"api/sns/v1/lit/account/account_info"
"api/sns/v1/lit/account/pay_discount_inform"
"api/sns/v1/lit/image/upload"
"api/sns/v1/lit/oss/get_sts_token"
"api/sns/v1/lit/user/firebase_token"
"api/sns/v1/lit/user_visit/get_visit_nums"
"api/sns/v1/lit/match_history/matched_history"
"api/sns/v1/lit/gift/received_gifts_num"
"api/sns/v1/lit/mood_status/set_status"
"api/sns/v1/lit/user_tag/tags?class=v2"
"api/sns/v1/lit/user/conversation"
"api/sns/v1/lit/user/register_brand_token_by_uuid"
"api/sns/v1/lit/user/cover_photo"
"api/sns/v1/lit/block/{user}"
"api/sns/v1/lit/user_tag/user_tags/{id}"
"api/sns/v1/lit/user/del_conversation/{conversation_id}"
"api/sns/v1/lit/get_email_code"
"api/sns/v1/lit/remove_follower"
"api/sns/v1/lit/user/query_online_and_partyid"
"api/sns/v1/lit/user/del_conversations"
"api/sns/v1/lit/user/get_secondary_names"
"api/sns/v1/lit/user/user_bind_email"
"api/sns/v1/lit/blocks"
"api/sns/v1/lit/user/accost_others"
"api/sns/v1/lit/taptap/new_taptap"
"api/sns/v1/lit/taptap/taptap_record"
"api/sns/v1/lit/user/user_bind_phone"
"api/sns/v1/lit/home/report"
"api/sns/v1/lit/user_visit/visited_list"
"api/sns/v1/lit/match_history/{path}"
"api/sns/v1/lit/user/conversations"
"api/sns/v1/lit/user/other_info"
"api/sns/v1/lit/mood_status/home"
"api/sns/v1/lit/follow/{user}"
"api/sns/v1/lit/gift/received_gifts_contributor"
"api/sns/v1/lit/user/accost_count"
"api/sns/v1/lit/follower"
"api/sns/v1/lit/unfollow/{user}"
"api/sns/v1/lit/account/buy_avatar/{avatar}"
"api/sns/v1/lit/user/firebase_token_uuid"
"api/sns/v1/lit/user/link_spotify"
"api/sns/v1/lit/user/cancel_del"
"api/sns/v1/lit/user/update_secondary_name"
"api/sns/v1/lit/following"
"api/sns/v1/lit/block_upload_chat"
"api/sns/v1/lit/unblock/{user}"
"api/sns/v1/lit/user/update_loc"
"api/sns/v1/lit/user_visit/all_viewed"
"api/sns/v1/lit/user/user_contact_info"
"api/sns/v1/lit/mood_status/same_mood_users"
"api/sns/v1/lit/user/judge_video"
"api/sns/v1/lit/user_tag/ensure_tags"
"api/sns/v1/lit/user/message_list"
"api/sns/v1/lit/user/read_messages"
"api/sns/v1/lit/user/message_notifications"
"api/sns/v1/lit/multiplayer_box/party_func"
"api/sns/v1/lit/party/party_unfollow"
"api/sns/v1/lit/gift/new_comer_gifts"
"api/sns/v1/lit/party/quick_follow"
"api/sns/v1/lit/party/room_level_info"
"api/sns/v1/lit/party/room_level_info"
"api/sns/v1/lit/party/party_banners?position=1"
"api/sns/v1/lit/party/quit_party"
"api/sns/v1/lit/party/get_party_info/{party_id}"
"api/sns/v1/lit/party/change_entry_message_merged"
"api/sns/v1/lit/party/enter_room"
"api/sns/v1/lit/party/party_follow"
"api/sns/v1/lit/party/change_party_welcome"
"api/sns/v1/lit/party/slide_rooms"
"api/sns/v1/lit/party/party_other_info"
"api/sns/v1/lit/party/change_party_info"
"api/sns/v1/lit/party/party_send_pic"
"api/sns/v1/lit/cloud_music/upload_music"
"api/sns/v1/lit/friend"
"api/sns/v1/lit/user/get_users_info"
"api/sns/v1/lit/party/top_three"
"api/sns/v1/lit/multiplayer_box/party_func"
"api/sns/v1/lit/party/query_receive_level"
"api/sns/v1/lit/party/restart_party_diamonds"
"api/sns/v1/lit/propose/change_ring"
"api/sns/v1/lit/party/set_party_pwd"
"api/sns/v1/lit/party/remove_banner"
"api/sns/v1/lit/propose/lover_home"
"api/sns/v1/lit/party/get_local_rank_info"
"api/sns/v1/lit/party_challenge/get_party_challenge_resource"
"api/sns/v1/lit/party/change_room_mode"
"api/sns/v1/lit/party/for_u"
"api/sns/v1/lit/party/party_send_diamonds_rain"
"api/sns/v1/lit/propose/show_novice_tutorial"
"api/sns/v1/lit/party/show_followed_party"
"api/sns/v1/lit/party/grant_recharge_bonus"
"api/sns/v1/lit/party/add_song"
"api/sns/v1/lit/party/recharge_bonus_setting"
"api/sns/v1/lit/party/avatar_expressions"
"api/sns/v1/lit/party/party_banners"
"api/sns/v1/lit/party/send_party_gifts"
"api/sns/v1/lit/party/remove_song"
"api/sns/v1/lit/account/send_blind_gift"
"api/sns/v1/lit/party/invite_user_infos"
"api/sns/v1/lit/party_challenge/switch_challenge"
"api/sns/v1/lit/party/followed_party"
"api/sns/v1/lit/party/get_party_search_discovery_result"
"api/sns/v1/lit/party/get_party_tags"
"api/sns/v1/lit/gift/bag_management_rule"
"api/sns/v1/lit/party/create_party"
"api/sns/v1/lit/party/get_party_search_discovery"
"api/sns/v1/lit/party/get_party_info/{party_id}"
"api/sns/v1/lit/party/get_send_gift_detail"
"api/sns/v1/lit/party/party_followers"
"api/sns/v1/lit/party/invite_friends_list"
"api/sns/v1/lit/party/party_red_packets_num"
"api/sns/v1/lit/party/get_token"
"api/sns/v1/lit/party/party_heat_start"
"api/sns/v1/lit/party/kick_and_lock_mic"
"api/sns/v1/lit/party/change_lock_status"
"api/sns/v1/lit/party/get_local_rank_info"
"api/sns/v1/lit/party/invite_family_member_list"
"api/sns/v1/lit/party/switch_block_chat"
"api/sns/v1/lit/party/change_mute"
"api/sns/v1/lit/party/random_join_party"
"api/sns/v1/lit/party/get_play_list"
"api/sns/v1/lit/party/search_party"
"api/sns/v1/lit/gift/gift_banner"
"api/sns/v1/lit/party/quit_party"
"api/sns/v1/lit/party/diamonds_lucky_animation"
"api/sns/v1/lit/party/new_set_admin"
"api/sns/v1/lit/party/chat_mic_action"
"api/sns/v1/lit/party/get_banner_list"
"api/sns/v1/lit/party/chat_invite_to_mic"
"api/sns/v1/lit/party/unset_admin"
"api/sns/v1/lit/party/kick_out_new"
"api/sns/v1/lit/propose/click_propose_letter"
"api/sns/v1/lit/party/switch_mute_mic"
"api/sns/v1/lit/gift/gifts_num_choice"
"api/sns/v1/lit/party/get_global_rank_info"
"api/sns/v1/lit/propose/broke"
"api/sns/v1/lit/party/invite_followers"
"api/sns/v1/lit/propose/set_propose_status"
"api/sns/v1/lit/party_challenge/party_challenge_settlement"
"api/sns/v1/lit/party/party_diamonds_rain_config"
"api/sns/v1/lit/party_challenge/get_challenge_rank"
"api/sns/v1/lit/party/lucky_draw"
"api/sns/v1/lit/party/offline_mic"
"api/sns/v1/lit/party/get_virtual_party_id"
"api/sns/v1/lit/party/get_tag_party_list"
"api/sns/v1/lit/party/get_home_party_info/{user_id}"
"api/sns/v1/lit/account/send_ring"
"api/sns/v1/lit/party/party_heat_stop"
"api/sns/v1/lit/propose/collect_balloon"
"api/sns/v1/lit/party/party_member_num"
"api/sns/v1/lit/party/song_origin_volume"
"api/sns/v1/lit/sound_effect/sound_effects"
"api/sns/v1/lit/party/query_sent_level"
"api/sns/v1/lit/party/register_party_action"
"api/sns/v1/lit/party/dissolve_party"
"api/sns/v1/lit/party/invite_friends"
"api/sns/v1/lit/party/recent"
"api/sns/v1/lit/party/accept_invite_mic"
"api/sns/v1/lit/party/check_members"
"api/sns/v1/lit/cloud_music/end_music"
"api/sns/v1/lit/propose/lover_home"
"api/sns/v1/lit/party/invite_to_admin"
"api/sns/v1/lit/cloud_music/start_music"
"api/sns/v1/lit/crystal_park/lucky_star_exchange"
"api/sns/v1/lit/crystal_park/exchange_record"
"api/sns/v1/lit/crystal_park/draw_lottery"
"api/sns/v1/lit/crystal_park/crystal_park_record"
"api/sns/v1/lit/crystal_park/exchange_shop"
"api/sns/v1/lit/crystal_park/get_resource_info"
"api/sns/v1/lit/crystal_park/get_choices"
"api/sns/v1/lit/crystal_park/crystal_park_rank"
"api/sns/v1/lit/family/handle_member_changes"
"api/sns/v1/lit/family/get_my_family_info"
"api/sns/v1/lit/family/invitation/sent_record"
"api/sns/v1/lit/family/get_family_home_info"
"api/sns/v1/lit/family/get_family_square_info"
"api/sns/v1/lit/family/invitation/setting"
"api/sns/v1/lit/family/want_family/set_declaration"
"api/sns/v1/lit/family/assets/donate"
"api/sns/v1/lit/family/send_shared_info"
"api/sns/v1/lit/family/share_follower_list"
"api/sns/v1/lit/family_weekly_treasure_box/progress"
"api/sns/v1/lit/family/want_family/home_info"
"api/sns/v1/lit/family/want_family/users"
"api/sns/v1/lit/family/invitation/received_record"
"api/sns/v1/lit/family/handle_member_changes"
"api/sns/v1/lit/family/get_family_feeds"
"api/sns/v1/lit/family/search_family"
"api/sns/v1/lit/family/dissolve_family"
"api/sns/v1/lit/family/get_apply_record"
"api/sns/v1/lit/family/missions/claim_status"
"api/sns/v1/lit/family/update_family_info"
"api/sns/v1/lit/family/create_family"
"api/sns/v1/lit/family/get_handled_record"
"api/sns/v1/lit/family/invitation/send"
"api/sns/v1/lit/family/del_leave_code"
"api/sns/v1/lit/family/get_family_members_info"
"api/sns/v1/lit/intimate_friend/break_up"
"api/sns/v1/lit/intimate_friend/change_friend_souvenir"
"api/sns/v1/lit/intimate_friend/home"
"api/sns/v1/lit/intimate_friend/reject_request"
"api/sns/v1/lit/intimate_friend/send_friend_souvenir"
"api/sns/v1/lit/intimate_friend/click_friend_letter"
"api/sns/v1/lit/intimate_friend/is_friend"
"api/sns/v1/lit/intimate_friend/accept_request"
"api/sns/v1/lit/friend"
"api/sns/v1/lit/party/party_heat_start"
"api/sns/v1/lit/party/party_heat_card_product"
"api/sns/v1/lit/party/party_heat_status_for_host"
"api/sns/v1/lit/party/get_own_party"
"api/sns/v1/lit/lit_bank"
"api/sns/v1/lit/lit_bank/is_claimable"
"api/sns/v1/lit/lit_bank/sku_info"
"api/sns/v1/lit/lit_bank/switch"
"api/sns/v1/lit/lit_pass/claim_level_rewards"
"api/sns/v1/lit/lit_pass/user_score"
"api/sns/v1/lit/lit_pass/user_missions"
"api/sns/v1/lit/lit_pass/buy_level"
"api/sns/v1/lit/lit_pass/claim_mission"
"api/sns/v1/lit/lit_pass/boost_rewards"
"api/sns/v1/lit/lit_pass/claim_daily_count_mission"
"api/sns/v1/lit/lit_pass/litpass_rewards"
"api/sns/v1/lit/lit_pass/user_need_claim"
"api/sns/v1/lit/lit_pass/sku_info"
"api/sns/v1/lit/lit_pass/show_popup"
"api/sns/v1/lit/lit_pass/level_score_rank_page_info"
"api/sns/v1/lit/mic_emoj_interaction"
"api/sns/v1/lit/upcoming_activity/sub_or_unsub_activity"
"api/sns/v1/lit/upcoming_activity/create_activity"
"api/sns/v1/lit/upcoming_activity/show_red_dot"
"api/sns/v1/lit/upcoming_activity/my_activity"
"api/sns/v1/lit/upcoming_activity/end_activity"
"api/sns/v1/lit/party/party_banners"
"api/sns/v1/lit/upcoming_activity/get_activity_info_by_id"
"api/sns/v1/lit/upcoming_activity/backgrounds"
"api/sns/v1/lit/upcoming_activity/get_exam_user_tag"
"api/sns/v1/lit/upcoming_activity/update_activity_info"
"api/sns/v1/lit/upcoming_activity/activity_square"
"api/sns/v1/lit/party/auction/bid"
"api/sns/v1/lit/party/auction"
"api/sns/v1/lit/party/user_dynamic_backgrounds"
"api/sns/v1/lit/party/party_background"
"api/sns/v1/lit/party/party_layouts"
"api/sns/v1/lit/account/buy_party_layout"
"api/sns/v1/lit/party/change_party_background"
"api/sns/v1/lit/party/user_party_layouts"
"api/sns/v1/lit/party/change_mode_and_layout"
"api/sns/v1/lit/account/buy_dynamic_background"
"api/sns/v1/lit/party/dynamic_backgrounds"
"api/sns/v1/lit/account/buy_party_background"
"api/sns/v1/lit/party/user_party_background"
"api/sns/v1/lit/party/change_party_layout"
"api/sns/v1/lit/party/change_party_dynamic_background"
"api/sns/v1/lit/party/switch_calculator"
"api/sns/v1/lit/party/calculator_choice"
"api/sns/v1/lit/party/get_calculator_contributor"
"api/sns/v1/lit/home/user_feedback"
"api/sns/v1/lit/home/feedback"
"api/sns/v1/lit/home/user_feedback"
"api/sns/v1/lit/user/info_by_huanxin"
"api/sns/v1/lit/image/upload"
"api/sns/v1/lit/tool/translate"
"api/sns/v1/lit/user/self_in_app_msg"
"api/sns/v1/lit/party/pks"
"api/sns/v1/lit/party/pks"
"api/sns/v1/lit/party/pks"
"api/sns/v1/lit/party/pks/duration_choice"
"api/sns/v1/lit/party/pks/vote"
"api/sns/v1/lit/user/zone/{userId}"
"api/sns/v1/lit/recharge_bonus/banner"
"api/sns/v1/lit/vip/reward_daily_diamonds"
"api/sns/v1/lit/vip/home"
"api/sns/v1/lit/vip/privilege"
"api/sns/v1/lit/vip/daily_diamonds_info"
"api/sns/v1/lit/feed/change_visibility/{id}"
"api/sns/v1/lit/feed/recommend_tags"
"api/sns/v1/lit/feed/tag_search"
"api/sns/v1/lit/user/get_mention_list"
"api/sns/v1/lit/feed/create"
"api/sns/v1/lit/feed/reference_list/{feed_id}"
"api/sns/v1/lit/feed/anon"
"api/sns/v1/lit/feed/my_anonymous_feeds"
"api/sns/v1/lit/feed/info/{feed_id}"
"api/sns/v1/lit/feed/react/{feed_id}"
"api/sns/v1/lit/feed/feed_page_structure"
"api/sns/v1/lit/home/get_filters"
"api/sns/v1/lit/home/user_filters"
"api/sns/v1/lit/home/same_city_users"
"api/sns/v1/lit/home/report_gps"
"api/sns/v1/lit/account/city_card_product"
"api/sns/v1/lit/user_tag/user_tags/{id}"
"api/sns/v1/lit/user_tag/ensure_tags"
"api/sns/v1/lit/user_tag/tags?class=v2"
"api/sns/v1/lit/handbook/receive_rewards"
"api/sns/v1/lit/handbook/schedule"
"api/sns/v1/lit/handbook/resource_info"
"api/sns/v1/lit/handbook/get_handbook"
"api/sns/v1/lit/family/family_shop"
"api/sns/v1/lit/account/buy_resource"
"api/sns/v1/lit/shop/banner_info"
"api/sns/v1/lit/resources/resources_bag"
"api/sns/v1/lit/shop/latest_resources"
"api/sns/v1/lit/contact/{type}"
"api/sns/v1/lit/gift/detail_info_by_type_and_id"
"api/sns/v1/lit/shop/resources/{resource_type}"
"api/sns/v1/lit/family/family_shop/buy"
"api/sns/v1/lit/resources/resources_shop"
"api/sns/v1/lit/resources/change_resource"
"api/sns/v1/lit/resources/prefetch"
"api/sns/v1/lit/owner_withdraw/apply_withdraw"
"api/sns/v1/lit/feed/create"
"api/sns/v1/lit/audio/upload"
"api/sns/v1/lit/feed/view/{user}"
"api/sns/v1/lit/user/profile_cards"
"api/sns/v1/lit/home/online_users"
```

(There may be duplicated entry)

You can find all the endpoints and their info by searching for `value = "api/` in the disassembled APK.

## III. Logging
The logging is using [Tencent's Mars Logging Library](https://github.com/Tencent/mars/tree/master/mars/log) and
encrypted using a public key. The log will be uploaded to Litatom.

To enable logging (For reversing), you can hook into the library itself using Frida, it will also print out if the SSL Unpinning is successfully or not.

## IV. Encryption
Request bodies and some of the response bodies (That has `application/x-litatom-json` as content type)
are encrypted using `LibGuard`. There are also pure-java encryption method
included in the APK, it's used to encrypt Chat messages, encrypt basic parameters
(For SMS Login, Google Login, FaceBook Login, or Get User Info endpoints, and 
a weird one (check if it's contains `sgposs` in host?)).

The keys could be extracted from `com.lit.app.net.interceptors(?).BasicParamsInterceptor`
(Name is deobfuscated with the proguard rules applied and debug annotations kept in
compiled Kotlin bytecode). This 
includes the key that's used to encrypt chat messages as it's duplicated, but
if it's changed it could be extracted from `com.lit.app.im.IMModel` class (Obfuscated)


Here's the extracted keys for the current version
```js
SGPOSS_KEY = "AC0A60D491D9876D1012FB24DB61ADC6"
SECURE_ENDPOINTS_KEY = "CB7F786FC0E6E105E6DA03D1FFF05C0F"
CHAT_KEY = "CB7F786FC0E6E105E6DA03D1FFF05C0F"
MODE_1_KEY = "CB7F786FC0E6E105E6DA03D1FFF05C0F"
MODE_2_KEY = "EIOWUGWOERGJKNLDKGJFOI879KJNSDKJ"
MODE_3_KEY = "f1c9208ccd8ef6d85c44b451da593cd4"
MODE_4_KEY = "AC0A60D491D9876D1012FB24DB61ADC6"
MODE_5_KEY = "LTMWUGWOBNLJKIOEKGJFOI256KIOWNKF"
```

As mentioend above, Libguard mode 3 is a little more secure, it uses random with `time()` as seed, 
and generate 16 bytes of IV parameter. Then it appends the generated IV to the encrypted token, than Base64 it. LibGuard also uses a different Base64 mapping:
```kt
fun base64DecodeTransformLibGuard(data: String): String {
    return data.replace("-", "+")
        .replace("_", "/")
        .replace(".", "=")
}
fun base64EncodeTransformLibGuard(data: String): String {
    return data.replace("+", "-")
        .replace("/", "_")
        .replace("=", ".")
}
```

We suspect it's there because it doesn't need to escape `/` and `+` for url, and also strip it a little so it's harder to figure out what it's about.

## Conclusion, what we've learned
We've found a few problems with Litmatch. First, obviously is the request and response
encryption. It's using AES, which is not really secure for man-in-the-middle attack,
there's basically no reason of using AES from security standpoint. A RSA encryption
could improve things, so it will be much more difficult to reverse Http requests by
simply decrypting them - because we don't have the private key.

It's also using a fixed Initial Vector Parameter for AES in both LibGuard encryption
mode 1, 2, 4, 5, and pure-java encryption (It's supposed to be random. but in the code
it's always `abcdef1234567890`), while mode 3 is the s standard way of AES CBC encryption.

From a Minecraft premium client developer standpoint, the obfuscation is too weak, we
do know that most Android apps don't need obfuscation, but Proguard isn't even stripping
the source file name, which I find it really weird, With source file name stripped,
it would be much much harder to reverse.

It seems like everything is in conflict to us, it got RSA for logging encryption
, but then it uses AES with fixed IV to encrypt and decrypt requests and responses;
It got `libguard` as native library, while it could be easily implemented with Java or
Kotlin, which sounds like they want to prevent reversers, but they didn't even
bother to remove function names from the native library, or even remove source file name
from compiled Kotlin classes.

I have no mean to say that Construct Tech is bad, because compare to 90% of the apps on
the market, it's secure enough, but there are definitely room for improvement.

<br>
<br>

<p align="center">(c) fan87, TropicalFan344  All rights reserves</p>

