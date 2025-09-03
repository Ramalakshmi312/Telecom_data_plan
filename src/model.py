import pandas as pd

def recommend_plans_simple(user_profile, all_users_profiles, plans_df, n=5):
    """
    Recommend plans based on similarity of usage profiles and budget filter.
    
    :param user_profile: dict with keys 'data_usage', 'call_minutes', 'sms_count', 'budget'
    :param all_users_profiles: DataFrame with user profiles (must include columns matching keys above plus 'current_plan')
    :param plans_df: DataFrame with available plans (columns include 'planName', 'price')
    :param n: Number of recommendations to return
    :return: DataFrame of recommended plans
    """
    # Calculate Euclidean distance between user and all others based on usage stats
    def usage_distance(row):
        return ((row['data_usage'] - user_profile.get('data_usage', 0))**2 +
                (row['call_minutes'] - user_profile.get('call_minutes', 0))**2 +
                (row['sms_count'] - user_profile.get('sms_count', 0))**2) ** 0.5
    
    all_users_profiles['distance'] = all_users_profiles.apply(usage_distance, axis=1)
    
    # Exclude current user from comparison if email/id available (optional)
    # For example, drop user with matching email if user_profile has 'email'
    
    # Select top n closest users
    similar_users = all_users_profiles.nsmallest(n, 'distance')
    
    # Aggregate the popular plans among similar users
    popular_plans = similar_users['current_plan'].value_counts().index.tolist()
    
    # Filter plans within budget
    budget = user_profile.get('budget', float('inf'))
    affordable_plans = plans_df[plans_df['price'] <= budget]
    
    # Select plans recommended popular by similar users within budget
    recommended_plans = affordable_plans[affordable_plans['planName'].isin(popular_plans)]
    
    # If not enough recommendations, fallback to top affordable plans by price ascending
    if len(recommended_plans) < n:
        remainder = min(n - len(recommended_plans), len(affordable_plans))
        fallback = affordable_plans[~affordable_plans['planName'].isin(popular_plans)].sort_values('price').head(remainder)
        recommended_plans = pd.concat([recommended_plans, fallback])
    
    return recommended_plans.head(n)
