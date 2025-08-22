from sqlalchemy import select, func, and_
from sqlalchemy.orm import aliased

from src.domain.portfolio_performances.portfolio_performance_model import (
    PortfolioPerformance,
)


def get_performance_status(portfolio_id, status_date=None):
    cte_dates = (
        select(
            PortfolioPerformance.portfolio_id,
            PortfolioPerformance.date,
            (
                func.lag(PortfolioPerformance.date).over(
                    order_by=PortfolioPerformance.date.asc()
                )
            ).label("previous_date"),
            func.max(PortfolioPerformance.date).over().label("max_date"),
        ).where(PortfolioPerformance.portfolio_id == portfolio_id)
    ).cte("cte_dates")

    cte_status_dates = (
        select(cte_dates)
        .where(cte_dates.c.date == func.coalesce(status_date, cte_dates.c.max_date))
        .cte("cte_status_dates")
    )

    curr_perf = aliased(PortfolioPerformance, name="curr_perf")
    prev_perf = aliased(PortfolioPerformance, name="prev_perf")

    query = (
        select(
            cte_status_dates.c.date,
            curr_perf.market_value,
            (curr_perf.market_value - prev_perf.market_value).label(
                "market_value_delta"
            ),
            (curr_perf.market_value / prev_perf.market_value - 1).label(
                "market_value_delta_pct"
            ),
            curr_perf.cash_balance,
            (curr_perf.cash_balance - prev_perf.cash_balance).label(
                "cash_balance_delta"
            ),
            (curr_perf.cash_balance / prev_perf.cash_balance - 1).label(
                "cash_balance_delta_pct"
            ),
            curr_perf.invested_amount,
            (curr_perf.invested_amount - prev_perf.invested_amount).label(
                "invested_amount_delta"
            ),
            (curr_perf.invested_amount / prev_perf.invested_amount - 1).label(
                "invested_amount_delta_pct"
            ),
            curr_perf.invested_amount_total,
            (curr_perf.invested_amount_total - prev_perf.invested_amount_total).label(
                "invested_amount_total_delta"
            ),
            (
                curr_perf.invested_amount_total / prev_perf.invested_amount_total - 1
            ).label("invested_amount_total_delta_pct"),
            curr_perf.asset_disposal_income,
            (curr_perf.asset_disposal_income - prev_perf.asset_disposal_income).label(
                "asset_disposal_income_delta"
            ),
            (
                curr_perf.asset_disposal_income / prev_perf.asset_disposal_income - 1
            ).label("asset_disposal_income_delta_pct"),
            curr_perf.asset_disposal_income_total,
            (
                curr_perf.asset_disposal_income_total
                - prev_perf.asset_disposal_income_total
            ).label("asset_disposal_income_total_delta"),
            (
                curr_perf.asset_disposal_income_total
                / prev_perf.asset_disposal_income_total
                - 1
            ).label("asset_disposal_income_total_delta_pct"),
            curr_perf.asset_holding_income,
            (curr_perf.asset_holding_income - prev_perf.asset_holding_income).label(
                "asset_holding_income_delta"
            ),
            (curr_perf.asset_holding_income / prev_perf.asset_holding_income - 1).label(
                "asset_holding_income_delta_pct"
            ),
            curr_perf.asset_holding_income_total,
            (
                curr_perf.asset_holding_income_total
                - prev_perf.asset_holding_income_total
            ).label("asset_holding_income_total_delta"),
            (
                curr_perf.asset_holding_income_total
                / prev_perf.asset_holding_income_total
                - 1
            ).label("asset_holding_income_total_delta_pct"),
            curr_perf.interest_income,
            (curr_perf.interest_income - prev_perf.interest_income).label(
                "interest_income_delta"
            ),
            (curr_perf.interest_income / prev_perf.interest_income - 1).label(
                "interest_income_delta_pct"
            ),
            curr_perf.interest_income_total,
            (curr_perf.interest_income_total - prev_perf.interest_income_total).label(
                "interest_income_total_delta"
            ),
            (
                curr_perf.interest_income_total / prev_perf.interest_income_total - 1
            ).label("interest_income_total_delta_pct"),
            curr_perf.investment_income,
            (curr_perf.investment_income - prev_perf.investment_income).label(
                "investment_income_delta"
            ),
            (curr_perf.investment_income / prev_perf.investment_income - 1).label(
                "investment_income_delta_pct"
            ),
            curr_perf.investment_income_total,
            (
                curr_perf.investment_income_total - prev_perf.investment_income_total
            ).label("investment_income_total_delta"),
            (
                curr_perf.investment_income_total / prev_perf.investment_income_total
                - 1
            ).label("investment_income_total_delta_pct"),
            curr_perf.profit,
            (curr_perf.profit - prev_perf.profit).label("profit_delta"),
            (curr_perf.profit / prev_perf.profit - 1).label("profit_delta_pct"),
            curr_perf.profit_total,
            (curr_perf.profit_total - prev_perf.profit_total).label(
                "profit_total_delta"
            ),
            (curr_perf.profit_total / prev_perf.profit_total - 1).label(
                "profit_total_delta_pct"
            ),
            curr_perf.profit_percentage,
            (curr_perf.profit_percentage - prev_perf.profit_percentage).label(
                "profit_percentage_delta"
            ),
            (curr_perf.profit_percentage / prev_perf.profit_percentage - 1).label(
                "profit_percentage_delta_pct"
            ),
            curr_perf.profit_percentage_total,
            (
                curr_perf.profit_percentage_total - prev_perf.profit_percentage_total
            ).label("profit_percentage_total_delta"),
            (
                curr_perf.profit_percentage_total / prev_perf.profit_percentage_total
                - 1
            ).label("profit_percentage_total_delta_pct"),
            curr_perf.drawdown_value,
            (curr_perf.drawdown_value - prev_perf.drawdown_value).label(
                "drawdown_value_delta"
            ),
            (1 - curr_perf.drawdown_value / prev_perf.drawdown_value).label(
                "drawdown_value_delta_pct"
            ),
            curr_perf.drawdown_value_total,
            (curr_perf.drawdown_value_total - prev_perf.drawdown_value_total).label(
                "drawdown_value_total_delta"
            ),
            (1 - curr_perf.drawdown_value_total / prev_perf.drawdown_value_total).label(
                "drawdown_value_total_delta_pct"
            ),
            curr_perf.drawdown_profit,
            (curr_perf.drawdown_profit - prev_perf.drawdown_profit).label(
                "drawdown_profit_delta"
            ),
            (1 - curr_perf.drawdown_profit / prev_perf.drawdown_profit).label(
                "drawdown_profit_delta_pct"
            ),
            curr_perf.drawdown_profit_total,
            (curr_perf.drawdown_profit_total - prev_perf.drawdown_profit_total).label(
                "drawdown_profit_total_delta"
            ),
            (
                1 - curr_perf.drawdown_profit_total / prev_perf.drawdown_profit_total
            ).label("drawdown_profit_total_delta_pct"),
            curr_perf.drawdown,
            (curr_perf.drawdown - prev_perf.drawdown).label("drawdown_delta"),
            (1 - curr_perf.drawdown / prev_perf.drawdown).label("drawdown_delta_pct"),
            curr_perf.twrr_rate_daily,
            (curr_perf.twrr_rate_daily - prev_perf.twrr_rate_daily).label(
                "twrr_rate_daily_delta"
            ),
            (curr_perf.twrr_rate_daily / prev_perf.twrr_rate_daily - 1).label(
                "twrr_rate_daily_delta_pct"
            ),
            curr_perf.twrr_rate_annualized,
            (curr_perf.twrr_rate_annualized - prev_perf.twrr_rate_annualized).label(
                "twrr_rate_annualized_delta"
            ),
            (curr_perf.twrr_rate_annualized / prev_perf.twrr_rate_annualized - 1).label(
                "twrr_rate_annualized_delta_pct"
            ),
            curr_perf.sharpe_ratio_daily,
            (curr_perf.sharpe_ratio_daily - prev_perf.sharpe_ratio_daily).label(
                "sharpe_ratio_daily_delta"
            ),
            (curr_perf.sharpe_ratio_daily / prev_perf.sharpe_ratio_daily - 1).label(
                "sharpe_ratio_daily_delta_pct"
            ),
            curr_perf.sharpe_ratio_annualized,
            (
                curr_perf.sharpe_ratio_annualized - prev_perf.sharpe_ratio_annualized
            ).label("sharpe_ratio_annualized_delta"),
            (
                curr_perf.sharpe_ratio_annualized / prev_perf.sharpe_ratio_annualized
                - 1
            ).label("sharpe_ratio_annualized_delta_pct"),
            curr_perf.sortino_ratio_daily,
            (curr_perf.sortino_ratio_daily - prev_perf.sortino_ratio_daily).label(
                "sortino_ratio_daily_delta"
            ),
            (curr_perf.sortino_ratio_daily / prev_perf.sortino_ratio_daily - 1).label(
                "sortino_ratio_daily_delta_pct"
            ),
            curr_perf.sortino_ratio_annualized,
            (
                curr_perf.sortino_ratio_annualized - prev_perf.sortino_ratio_annualized
            ).label("sortino_ratio_annualized_delta"),
            (
                curr_perf.sortino_ratio_annualized / prev_perf.sortino_ratio_annualized
                - 1
            ).label("sortino_ratio_annualized_delta_pct"),
            curr_perf.xirr_rate,
            (curr_perf.xirr_rate - prev_perf.xirr_rate).label("xirr_rate_delta"),
            (curr_perf.xirr_rate / prev_perf.xirr_rate - 1).label(
                "xirr_rate_delta_pct"
            ),
            curr_perf.xirr_rate_total,
            (curr_perf.xirr_rate_total - prev_perf.xirr_rate_total).label(
                "xirr_rate_total_delta"
            ),
            (curr_perf.xirr_rate_total / prev_perf.xirr_rate_total - 1).label(
                "xirr_rate_total_delta_pct"
            ),
        )
        .join_from(
            cte_status_dates,
            curr_perf,
            and_(
                curr_perf.portfolio_id == cte_status_dates.c.portfolio_id,
                curr_perf.date == cte_status_dates.c.date,
            ),
        )
        .join(
            prev_perf,
            and_(
                prev_perf.portfolio_id == cte_status_dates.c.portfolio_id,
                prev_perf.date == cte_status_dates.c.previous_date,
            ),
        )
    )

    return query
