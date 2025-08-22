from sqlalchemy import insert, select, func, and_

from src.domain.portfolio_aggregate_performances.portfolio_aggregate_performance_model import (
    PortfolioAggregatePerformance,
)
from src.domain.portfolio_performances.portfolio_performance_model import (
    PortfolioPerformance,
)
from src.domain.portfolio_aggregates.portfolio_aggregate_model import PortfolioAggregate
from src.domain.portfolios.portfolio_model import Portfolio


def insert_with_select(user_id: int):
    cte_1 = (
        select(
            Portfolio.portfolio_aggregate_id,
            PortfolioAggregate.checkpoint_date,
            PortfolioPerformance.date,
            func.sum(PortfolioPerformance.market_value).label("market_value"),
            func.sum(PortfolioPerformance.market_value_adj).label("market_value_adj"),
            func.sum(PortfolioPerformance.delta_quantity_value_adj).label(
                "delta_quantity_value_adj"
            ),
            func.sum(PortfolioPerformance.cash_balance).label("cash_balance"),
            func.sum(PortfolioPerformance.invested_amount).label("invested_amount"),
            func.sum(PortfolioPerformance.invested_amount_total).label(
                "invested_amount_total"
            ),
            func.sum(PortfolioPerformance.asset_disposal_income).label(
                "asset_disposal_income"
            ),
            func.sum(PortfolioPerformance.asset_disposal_income_total).label(
                "asset_disposal_income_total"
            ),
            func.sum(PortfolioPerformance.asset_holding_income).label(
                "asset_holding_income"
            ),
            func.sum(PortfolioPerformance.asset_holding_income_total).label(
                "asset_holding_income_total"
            ),
            func.sum(PortfolioPerformance.interest_income).label("interest_income"),
            func.sum(PortfolioPerformance.interest_income_total).label(
                "interest_income_total"
            ),
            func.sum(PortfolioPerformance.investment_income).label("investment_income"),
            func.sum(PortfolioPerformance.investment_income_total).label(
                "investment_income_total"
            ),
            func.sum(PortfolioPerformance.profit).label("profit"),
            func.sum(PortfolioPerformance.profit_total).label("profit_total"),
        )
        .join_from(
            PortfolioPerformance,
            Portfolio,
            PortfolioPerformance.portfolio_id == Portfolio.id,
        )
        .join(
            PortfolioAggregate,
            PortfolioAggregate.id == Portfolio.portfolio_aggregate_id,
        )
        .where(
            and_(
                PortfolioAggregate.user_id == user_id,
                PortfolioPerformance.date >= PortfolioAggregate.checkpoint_date,
            )
        )
        .group_by(
            Portfolio.portfolio_aggregate_id,
            PortfolioPerformance.date,
        )
        .union_all(
            select(
                PortfolioAggregatePerformance.portfolio_aggregate_id,
                PortfolioAggregate.checkpoint_date,
                PortfolioAggregatePerformance.date,
                PortfolioAggregatePerformance.market_value,
                PortfolioAggregatePerformance.market_value_adj,
                PortfolioAggregatePerformance.delta_quantity_value_adj,
                PortfolioAggregatePerformance.cash_balance,
                PortfolioAggregatePerformance.invested_amount,
                PortfolioAggregatePerformance.invested_amount_total,
                PortfolioAggregatePerformance.asset_disposal_income,
                PortfolioAggregatePerformance.asset_disposal_income_total,
                PortfolioAggregatePerformance.asset_holding_income,
                PortfolioAggregatePerformance.asset_holding_income_total,
                PortfolioAggregatePerformance.interest_income,
                PortfolioAggregatePerformance.interest_income_total,
                PortfolioAggregatePerformance.investment_income,
                PortfolioAggregatePerformance.investment_income_total,
                PortfolioAggregatePerformance.profit,
                PortfolioAggregatePerformance.profit_total,
            )
            .join_from(
                PortfolioAggregatePerformance,
                PortfolioAggregate,
                PortfolioAggregate.id
                == PortfolioAggregatePerformance.portfolio_aggregate_id,
            )
            .where(
                and_(
                    PortfolioAggregate.user_id == user_id,
                    PortfolioAggregatePerformance.date
                    < PortfolioAggregate.checkpoint_date,
                )
            )
        )
        .cte(name="cte_1")
    )

    cte_2 = select(
        cte_1,
        (cte_1.c.profit / func.abs(cte_1.c.invested_amount)).label("profit_percentage"),
        (cte_1.c.profit_total / func.abs(cte_1.c.invested_amount_total)).label(
            "profit_percentage_total"
        ),
        func.max(cte_1.c.market_value + cte_1.c.asset_disposal_income)
        .over(
            partition_by=cte_1.c.portfolio_aggregate_id,
            order_by=cte_1.c.date,
        )
        .label("past_maximum_value"),
        func.max(cte_1.c.market_value + cte_1.c.asset_disposal_income_total)
        .over(
            partition_by=cte_1.c.portfolio_aggregate_id,
            order_by=cte_1.c.date,
        )
        .label("past_maximum_value_total"),
        func.max(cte_1.c.profit)
        .over(
            partition_by=cte_1.c.portfolio_aggregate_id,
            order_by=cte_1.c.date,
        )
        .label("past_maximum_profit"),
        func.max(cte_1.c.profit_total)
        .over(
            partition_by=cte_1.c.portfolio_aggregate_id,
            order_by=cte_1.c.date,
        )
        .label("past_maximum_profit_total"),
        func.coalesce(
            (
                (cte_1.c.market_value_adj - cte_1.c.delta_quantity_value_adj)
                / func.lag(cte_1.c.market_value_adj).over(
                    partition_by=cte_1.c.portfolio_aggregate_id,
                    order_by=cte_1.c.date,
                )
                - 1
            ),
            0.0,
        ).label("hpr"),
        (
            func.row_number().over(
                partition_by=cte_1.c.portfolio_aggregate_id,
                order_by=cte_1.c.date,
            )
        ).label("row_number"),
        (
            cte_1.c.invested_amount
            - func.lag(cte_1.c.invested_amount, 1, 0.0).over(
                partition_by=cte_1.c.portfolio_aggregate_id,
                order_by=cte_1.c.date,
            )
            + cte_1.c.investment_income
            - func.lag(cte_1.c.investment_income, 1, 0.0).over(
                partition_by=cte_1.c.portfolio_aggregate_id,
                order_by=cte_1.c.date,
            )
        ).label("cash_flow"),
        (
            cte_1.c.invested_amount_total
            - func.lag(cte_1.c.invested_amount_total, 1, 0.0).over(
                partition_by=cte_1.c.portfolio_aggregate_id,
                order_by=cte_1.c.date,
            )
            + cte_1.c.investment_income_total
            - func.lag(cte_1.c.investment_income_total, 1, 0.0).over(
                partition_by=cte_1.c.portfolio_aggregate_id,
                order_by=cte_1.c.date,
            )
        ).label("cash_flow_total"),
    ).cte(name="cte_2")

    cte_3 = select(
        cte_2,
        (
            func.exp(
                func.sum(func.ln(1 + cte_2.c.hpr)).over(
                    partition_by=cte_2.c.portfolio_aggregate_id,
                    order_by=cte_2.c.date,
                )
            )
        ).label("hpr_cumulative"),
        (cte_2.c.row_number / 365.0).label("years_passed"),
        func.nullif(cte_2.c.hpr, 0.0).label("hpr_non_zero"),
        (
            func.xirr(
                cte_2.c.date,
                cte_2.c.cash_flow,
                cte_2.c.market_value,
                cte_2.c.checkpoint_date,
            ).over(
                partition_by=cte_2.c.portfolio_aggregate_id,
                order_by=cte_2.c.date,
            )
        ).label("xirr_rate"),
        (
            func.xirr(
                cte_2.c.date,
                cte_2.c.cash_flow_total,
                cte_2.c.market_value,
                cte_2.c.checkpoint_date,
            ).over(
                partition_by=cte_2.c.portfolio_aggregate_id,
                order_by=cte_2.c.date,
            )
        ).label("xirr_rate_total"),
    ).cte(name="cte_3")

    cte_4 = select(
        cte_3,
        (
            func.max(cte_3.c.hpr_cumulative).over(
                partition_by=cte_3.c.portfolio_aggregate_id,
                order_by=cte_3.c.date,
            )
        ).label("past_maximum_hpr_cumulative"),
        (
            func.avg(cte_3.c.hpr_non_zero).over(
                partition_by=cte_3.c.portfolio_aggregate_id,
                order_by=cte_3.c.date,
            )
        ).label("hpr_non_zero_avg"),
        (
            func.stddev(cte_3.c.hpr_non_zero).over(
                partition_by=cte_3.c.portfolio_aggregate_id,
                order_by=cte_3.c.date,
            )
        ).label("hpr_non_zero_stddev"),
        (
            func.stddev(
                func.iif(cte_3.c.hpr_non_zero < 0, cte_3.c.hpr_non_zero, None)
            ).over(
                partition_by=cte_3.c.portfolio_aggregate_id,
                order_by=cte_3.c.date,
            )
        ).label("hpr_non_zero_stddev_d"),
        (
            func.count(cte_3.c.hpr_non_zero).over(
                partition_by=cte_3.c.portfolio_aggregate_id,
                order_by=cte_3.c.date,
            )
            * 365.0
            / cte_3.c.row_number
        ).label("avg_days_per_year"),
    ).cte(name="cte_4")

    query = select(
        cte_4.c.portfolio_aggregate_id,
        cte_4.c.date,
        cte_4.c.market_value,
        cte_4.c.market_value_adj,
        cte_4.c.delta_quantity_value_adj,
        cte_4.c.cash_balance,
        cte_4.c.invested_amount,
        cte_4.c.invested_amount_total,
        cte_4.c.asset_disposal_income,
        cte_4.c.asset_disposal_income_total,
        cte_4.c.asset_holding_income,
        cte_4.c.asset_holding_income_total,
        cte_4.c.interest_income,
        cte_4.c.interest_income_total,
        cte_4.c.investment_income,
        cte_4.c.investment_income_total,
        cte_4.c.profit,
        cte_4.c.profit_total,
        func.coalesce(cte_4.c.profit_percentage, 0.0).label("profit_percentage"),
        func.coalesce(cte_4.c.profit_percentage_total, 0.0).label(
            "profit_percentage_total"
        ),
        func.coalesce(
            (cte_4.c.market_value + cte_4.c.asset_disposal_income)
            / cte_4.c.past_maximum_value
            - 1,
            0.0,
        ).label("drawdown_value"),
        func.coalesce(
            (cte_4.c.market_value + cte_4.c.asset_disposal_income_total)
            / cte_4.c.past_maximum_value_total
            - 1,
            0.0,
        ).label("drawdown_value_total"),
        func.coalesce(
            (cte_4.c.profit - cte_4.c.past_maximum_profit) / cte_4.c.past_maximum_value,
            0.0,
        ).label("drawdown_profit"),
        func.coalesce(
            (cte_4.c.profit_total - cte_4.c.past_maximum_profit_total)
            / cte_4.c.past_maximum_value_total,
            0.0,
        ).label("drawdown_profit_total"),
        cte_4.c.hpr,
        (cte_4.c.hpr_cumulative / cte_4.c.past_maximum_hpr_cumulative - 1).label(
            "drawdown"
        ),
        (cte_4.c.hpr_cumulative - 1).label("twrr_rate_daily"),
        (func.pow(cte_4.c.hpr_cumulative, 1.0 / cte_4.c.years_passed) - 1).label(
            "twrr_rate_annualized"
        ),
        (cte_4.c.hpr_non_zero_avg / cte_4.c.hpr_non_zero_stddev).label(
            "sharpe_ratio_daily"
        ),
        (
            cte_4.c.hpr_non_zero_avg
            / cte_4.c.hpr_non_zero_stddev
            * func.pow(cte_4.c.avg_days_per_year, 0.5)
        ).label("sharpe_ratio_annualized"),
        (cte_4.c.hpr_non_zero_avg / cte_4.c.hpr_non_zero_stddev_d).label(
            "sortino_ratio_daily"
        ),
        (
            cte_4.c.hpr_non_zero_avg
            / cte_4.c.hpr_non_zero_stddev_d
            * func.pow(cte_4.c.avg_days_per_year, 0.5)
        ).label("sortino_ratio_annualized"),
        cte_4.c.xirr_rate,
        cte_4.c.xirr_rate_total,
    ).where(cte_4.c.date >= cte_4.c.checkpoint_date)

    return insert(PortfolioAggregatePerformance).from_select(
        [
            "portfolio_aggregate_id",
            "date",
            "market_value",
            "market_value_adj",
            "delta_quantity_value_adj",
            "cash_balance",
            "invested_amount",
            "invested_amount_total",
            "asset_disposal_income",
            "asset_disposal_income_total",
            "asset_holding_income",
            "asset_holding_income_total",
            "interest_income",
            "interest_income_total",
            "investment_income",
            "investment_income_total",
            "profit",
            "profit_total",
            "profit_percentage",
            "profit_percentage_total",
            "drawdown_value",
            "drawdown_value_total",
            "drawdown_profit",
            "drawdown_profit_total",
            "hpr",
            "drawdown",
            "twrr_rate_daily",
            "twrr_rate_annualized",
            "sharpe_ratio_daily",
            "sharpe_ratio_annualized",
            "sortino_ratio_daily",
            "sortino_ratio_annualized",
            "xirr_rate",
            "xirr_rate_total",
        ],
        query,
    )
