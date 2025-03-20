import logging
import nfl_data_py as nfl
import datetime
from constants import *

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

class NflStats:
    def __init__(self):
        self.latest_year_cache = None

    def get_latest_year(self):
        if self.latest_year_cache is None:
            try:
                current_year = datetime.datetime.now().year
                previous_year = current_year - 1
                df_current = nfl.import_weekly_data(years=[current_year])
                self.latest_year_cache = df_current['season'].max()
            except Exception as e:
                logger.error(f"Unable to get data for the current year: {e}. Trying Previous year")
                try:
                    df_previous = nfl.import_weekly_data(years=[previous_year])
                    self.latest_year_cache = df_previous['season'].max()
                except Exception as e:
                    logger.error(f"Error getting data for the previous year: {e}")
                    self.latest_year_cache = previous_year
        return self.latest_year_cache

    def speech_card_output(self, df, stat_type, top_n, week, year, const_begin_sentence, card_title):
        const_speech = f"{const_begin_sentence} week {week} year {year}"
        const_card_text = f"Week: {week}\nYear: {year}\n"
        players_desc = df.sort_values(by=[stat_type], ascending=False).iloc[0:top_n].to_dict(orient='records')[0]
        if stat_type in ['rushing_yards', 'rushing_tds']:
            speech = f"{const_speech}. {players_desc['player_display_name']} of {players_desc['recent_team']} carried {players_desc['carries']} times for {players_desc['rushing_yards']} yards and {players_desc['rushing_tds']} touch downs"
            card = f"""{const_card_text}Player: {players_desc['player_display_name']}\nTeam: {players_desc['recent_team']}\nPosition: {players_desc['position']}\nRushing Attempts: {players_desc['carries']}\nRushing Yards: {players_desc['rushing_yards']}\nRushing Touch Downs: {players_desc['rushing_tds']}"""
        elif stat_type in ['passing_yards', 'passing_tds']:
            speech = f"{const_speech}. {players_desc['player_display_name']} of {players_desc['recent_team']} completed {players_desc['completions']} out of {players_desc['attempts']} passing attempts for {players_desc['passing_yards']} yards. He threw {players_desc['passing_tds']} touch downs and {players_desc['interceptions']} picks"
            card = f"""{const_card_text}Player: {players_desc['player_display_name']}\nTeam: {players_desc['recent_team']}\nPosition: {players_desc['position']}\nPassing Attempts: {players_desc['attempts']}\nPassing Completions: {players_desc['completions']}\nPassing Yards: {players_desc['passing_yards']}\nPassing Touch Downs: {players_desc['passing_tds']}\nInterceptions: {players_desc['interceptions']}"""
        elif stat_type in ['receiving_yards', 'receiving_tds']:
            speech = f"{const_speech}. {players_desc['player_display_name']} of {players_desc['recent_team']} had {players_desc['receiving_yards']} yards. He was targeted {players_desc['targets']} times and had {players_desc['receiving_tds']} receiving touch downs"
            card = f"""{const_card_text}Player: {players_desc['player_display_name']}\nTeam: {players_desc['recent_team']}\nPosition: {players_desc['position']}\nReceiving Yards: {players_desc['receiving_yards']}\nTargets: {players_desc['targets']}\nReceiving Touch Downs: {players_desc['receiving_tds']}"""
        return speech, card_title, card

    def nfl_get_stat(self, year, week, stat_type, top_n=1):
        latest_year = self.get_latest_year()
        if year is not None and week is not None:
            logger.info(f"year is {year}")
            logger.info(f"week is {week}")
            try:
                year = int(year)
            except Exception as e:
                logger.info(f"Could not convert {year} to integer. Error: {e}")
                return FAIL_INSIDE_INTENT_MESSAGE
            try:
                week = int(week) if isinstance(week, int) else int(''.join([s for s in week if s.isdigit()]))
            except Exception as e:
                logger.info(f"Could not convert {week} to integer or list. Error: {e}")
                return FAIL_INSIDE_INTENT_MESSAGE
            logger.info(f"Year is: {year}")
            logger.info(f"Week is: {week}")
            if year < 1920:
                return NFL_DID_NOT_EXIST_THEN_MESSAGE
            elif year > latest_year:
                return FUTURE_YEAR_MESSAGE
            elif 1920 <= year < 1999:
                return NFL_STATS_DONT_EXIST_MESSAGE
            elif 1999 <= year <= latest_year:
                df = nfl.import_weekly_data([year])
                df = df[df['week'] == week]
                if stat_type in ['rushing_yards', 'rushing_tds', 'passing_yards', 'passing_tds', 'receiving_yards', 'receiving_tds']:
                    speech, card_title, card_text = self.speech_card_output(df, stat_type, top_n, week, year, RB_RESP_SENTENCE_BEGIN, RB_CARD_TITLE)
                    return speech, card_title, card_text
        return FAIL_INSIDE_INTENT_MESSAGE

nfl_stats = NflStats()