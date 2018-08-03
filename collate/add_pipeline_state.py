import sys
import csv
from sklearn import preprocessing
import numpy as np
import random
import datetime
import pandas as pd


###########################################
file_column_mappings = {
    "orders_after_2018-06-10_data_000": ["order_id", "map_attributes_imagery_dates", 
                                         "map_attributes_selected_imagery_date", "map_attributes_selected_version", 
                                         "map_attributes_source", "hyperion_attributes_allows_mfr", 
                                         "hyperion_attributes_is_mfr", "hyperion_attributes_is_prospect", 
                                         "hyperion_attributes_property_type", "hyperion_attributes_user_first_capture",
                                         "image_score", "deliverable_id", "deliverable_changed", "created_at", 
                                         "state", "site_id", "site_name", "sneaky", "local", "practice", 
                                         "priority", "roof_overlay", "failure_reason", "skip_markups"],
    
    "orders_after_2018-06-10_images_000": ["order_id", "score", "kind", "location", "distance", 
                                           "gps_accuracy", "make", "model"],
    
    "orders_after_2018-06-10_roof_visibility_000": ["order_id", "roof_visibility_attribute_ids"],
    
    "orders_after_2018-06-10_puborders_000": ["order_id", "order_state", "order_created_at", "order_updated_at", 
                                              "original_order_id", "order_complexity", "order_image_score", 
                                              "order_image_score_name", "priority", "order_deliverable", 
                                              "order_most_recent_failure_reason", "site_id", "order_local", 
                                              "slayer_job_id", "order_site_name", "sneaky", "order_skip_markups", 
                                              "number_of_stories", "e_number_of_stories_name", 
                                              "complexity_attributes_total_roof_facets_above_4_sqft", 
                                              "complexity_attributes_total_roof_facets", 
                                              "complexity_attributes_roof_square_footage", 
                                              "complexity_attributes_walls_square_footage", 
                                              "complexity_attributes_is_mfr", "map_attributes_source", 
                                              "slayer_attributes_allows_mfr", "slayer_attributes_is_mfr",
                                              "slayer_attributes_user_first_capture", "poser_release_number", 
                                              "structure_type", "structure_type_name", "poser_solve_status", 
                                              "hover_now", "first_qa_datetime", "first_qa_date", "models_reprocessed",
                                              "order_needs_to_be_reprocessed_flag", "special_request", "original_roof",
                                              "first_qa_for_state", "last_qa_for_state", "first_qa_email", 
                                              "first_qa_site_name", 
                                              "first_qa_majority_of_doors_within_95_percent_of_standard_sizes", 
                                              "first_qa_map_overlay_accurate", "first_qa_scale_within5_percent", 
                                              "first_qa_should_we_unfail_the_order", "qa_comments", "orthotag_list",
                                              "level_list", "pitch_estimate", "roof_estimate", 
                                              "labeler_roof_estimate", "markup_verifier_roof_estimate", 
                                              "markup_verifier_10_percent", "pitch_actual", "scaling_method",
                                              "visible_on_ortho_map", "door_areal_scale_diff", 
                                              "doors_used_for_scaling", "door_scale_deviation", "orthotag_tree_pass",
                                              "orthotag_poor_image_quality", "orthotag_none", 
                                              "orthotag_full_occlusion", "orthotag_not_on_map", 
                                              "orthotag_tree_occlusion", "orthotag_tree_fail", 
                                              "orthotag_missing_geometry", "orthotag_shadow", 
                                              "poser_solved_image_count", "poser_solved", "failed_complete_timeline", 
                                              "failed_complete_progression", "most_recent_failure_datetime", 
                                              "completed_count", "failed_count", "failed_or_complete_name_first",
                                              "failed_or_complete_name_second", "failed_or_complete_name_third", 
                                              "failed_or_complete_name_fourth", "failed_or_complete_name_fifth",
                                              "failed_or_complete_datetime_first", 
                                              "failed_or_complete_datetime_second", 
                                              "failed_or_complete_datetime_third", 
                                              "failed_or_complete_datetime_fourth",
                                              "failed_or_complete_datetime_fifth", "number_of_images",
                                              "average_image_score", "image_count_deleted", "image_count_0_sides",
                                              "image_count_1_side", "image_count_2_sides", "image_count_unscored", 
                                              "first_completion", "most_recent_completion", 
                                              "unfail_premium_order_flag", "turn_around_time_total", 
                                              "turn_around_time_first_completion", "total_resolution_time_total", 
                                              "total_resolution_time_first_completion", "human_bpo_time_waiting_total",
                                              "human_bpo_time_waiting_first_completion", "turn_around_time_wasted",
                                              "human_bpo_time_wasted", "labeling_time_total", 
                                              "labeling_time_first_completion", "markup_verifying_time_total",
                                              "markup_verifying_time_first_completion", "model_building_time_total",
                                              "model_building_time_first_completion", "modeling_time_total", 
                                              "modeling_time_first_completion", "model_completing_time_total", 
                                              "model_completing_time_first_completion", "web_segmenting_time_total",
                                              "web_segmenting_time_first_completion", "model_segmenting_time_total",
                                              "model_segmenting_time_first_completion", "verifying_time_total", 
                                              "verifying_time_first_completion", "texturing_time_total", 
                                              "texturing_time_first_completion", "qa_time_total", 
                                              "openings_marking_time_total", "openings_marking_time_first_completion",
                                              "vps_marking_time_total", "vps_marking_time_first_completion", 
                                              "primitive_marking_time_total", 
                                              "primitive_marking_time_first_completion"],
    
    "orders_after_2018-06-10_pubtasks_000": ["order_id", "state_transition_id", "transition_type", "transition_id",
                                             "image_id", "namespace", "event", "unlock_indicator", "from_state", 
                                             "to_state", "trigger_user_id", "seconds_in_state", 
                                             "transition_created_at", "image_markup_corrected_openings", 
                                             "image_markup_corrected_vps", "image_markup_corrected_primitive", 
                                             "image_markup_verify_result_reason_id_vps", "image_markup_verify_result_reason_id_openings", 
                                             "image_markup_verify_result_reason_id_primitive", "first_completion", 
                                             "most_recent_completion", "first_failure", "most_recent_failure", 
                                             "completion_time", "completion_count", "previous_completion_time", 
                                             "previous_completion_count", "total_completion_count", 
                                             "last_order_state_transition_id_of_type_before_complete", 
                                             "last_state_transition_of_type_before_complete_indicator", 
                                             "original_order_id", "order_current_state", "deliverable_name", 
                                             "order_image_score", "image_score_name", "sneaky", "order_complexity",
                                             "orders_most_recent_failure_reason_name", "skip_markups", 
                                             "complexity_attributes_is_mfr", "slayer_attributes_allows_mfr", 
                                             "slayer_attributes_is_mfr", "slayer_attributes_user_first_capture", 
                                             "poser_release_number", "structure_type", "poser_solve_status", "hover_now", 
                                             "map_attributes_source", "poser_solved_indicator", "order_site_name", 
                                             "modeler_email", "modeler_site_name", "modeler_roles", "resource_type", 
                                             "modeler_proficiency_level", "waiting_indicator", "unfail_premium_order_indicator"],
}

file_name_name_mapping = {
    #"orders_after_2018-06-10_data_000": "orders",
    #"orders_after_2018-06-10_images_000": "images",
    #"orders_after_2018-06-10_roof_visibility_000": "roof_visibility",
    "orders_after_2018-06-10_puborders_000": "puborders",
    #"orders_after_2018-06-10_pubtasks_000": "pubtasks",
}

###########################


# Load data and split into order_ids, features, labels
def load_init_data(data):
    order_ids = data[...,0]
    features = data[...,1:-1]
    labels = data[...,-1]
    return (order_ids, features, labels)

def get_state(pipeline_states, puborders, order_id):
    row = puborders[puborders['order_id'] == str(order_id)].iloc[0]
    timestamp = row['order_created_at']
    timestamp = datetime.datetime.strptime(timestamp.split(".")[0], "%Y-%m-%d %H:%M:%S")
    timestamp = timestamp.replace(second=0, microsecond=0)
    timestamp = timestamp.strftime("%Y-%m-%d %H:%M:%S")

    if row['failed_or_complete_name_first'] == 'failed':
        return None
    try:
        return pipeline_states[timestamp]
    except:
        return None

def normalize(order_states):
    all_states = None
    for order_id in order_states:
        state = order_states[order_id]
        if all_states is None:
            all_states = np.array(state)
        else:
            all_states = np.vstack((all_states, state))
    all_states_scaled = preprocessing.scale(all_states)
    normalized_states = {}
    for i in range(len(order_states)):
        order_id = list(order_states.keys())[i]
        normalized_states[order_id] = all_states_scaled[i]
    return normalized_states

def create_output_array(order_ids, init_features, labels, norm_order_states):
    stack = None
    for i in range(order_ids.shape[0]):
        order_id = order_ids[i]
        this_row = np.array([order_id])
        try:
            this_row = np.append(this_row, init_features[i])
            this_row = np.append(this_row, norm_order_states[order_id])
            this_row = np.append(this_row, labels[i])
        except:
            continue
        if stack is None:
            stack = this_row
        else:
            stack = np.vstack((stack, this_row))
    return stack

def load_puborders():
    print("Loading Data... ")
    data = {}
    for file_name, column_names in file_column_mappings.items():
        nice_name = file_name_name_mapping.get(file_name, None)
        if nice_name:
            print("Loading %s"%(nice_name))
            data[nice_name] = pd.read_csv("../data/%s" % file_name,
                                      sep='|',
                                      index_col=False, 
                                      names=column_names
                                    )
    print("Data Loaded!")
    return data['puborders']

def load_pipeline_states():
    output = {}
    rows = []
    with open('OrdersDataFrame.csv', 'r') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        for row in spamreader:
            rows.append(row)

    labels = rows[0]
    ignore = [0, 2, 18, 26]
    rows = rows[1:]

    for row in rows:
        time = datetime.datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S")
        feature = None
        for i in range(len(row)):
            if i in ignore:
                continue
            if feature is None:
                feature = np.array([float(row[i])])
            else:
                feature = np.append(feature, float(row[i]))
        output[time.strftime("%Y-%m-%d %H:%M:%S")] = feature
    return output

if __name__ == "__main__":
    pub_orders = load_puborders()
    pipeline_states = load_pipeline_states()

    order_ids, init_features, labels = \
        load_init_data(np.load('data.npy'))

    # Get states for all orders
    order_states = {}
    for order_id in order_ids:
        state = get_state(pipeline_states, pub_orders, int(order_id))
        if state is None:
            continue
        order_states[order_id] = state

    # Normalize states
    norm_order_states = \
        normalize(order_states)

    # Write to new data
    output_array = create_output_array(\
        order_ids, init_features, labels, norm_order_states)
    np.save('new_data_no_fail.npy', output_array)
