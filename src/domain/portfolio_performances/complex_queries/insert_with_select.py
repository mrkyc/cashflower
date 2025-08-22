from sqlalchemy import insert, select, and_, func

from src.domain.portfolio_performances.portfolio_performance_model import (
    PortfolioPerformance,
)
from src.domain.portfolio_group_performances.portfolio_group_performance_model import (
    PortfolioGroupPerformance,
)
from src.domain.adjusted_portfolio_transactions.adjusted_portfolio_transaction_model import (
    AdjustedPortfolioTransaction,
)
from src.domain.portfolios.portfolio_model import Portfolio
from src.domain.portfolio_aggregates.portfolio_aggregate_model import PortfolioAggregate


def insert_with_select(user_id: int):
    cte_portfolio_continuous_dates = (
        select(
            AdjustedPortfolioTransaction.portfolio_id,
            PortfolioAggregate.checkpoint_date,
            func.max(
                PortfolioAggregate.checkpoint_date,
                func.min(AdjustedPortfolioTransaction.date),
            ).label("date"),
        )
        .join_from(
            AdjustedPortfolioTransaction,
            Portfolio,
            Portfolio.id == AdjustedPortfolioTransaction.portfolio_id,
        )
        .join(
            PortfolioAggregate,
            PortfolioAggregate.id == Portfolio.portfolio_aggregate_id,
        )
        .where(PortfolioAggregate.user_id == user_id)
        .group_by(AdjustedPortfolioTransaction.portfolio_id)
        .cte(name="cte_portfolio_continuous_dates", recursive=True)
    )

    cte_portfolio_continuous_dates = cte_portfolio_continuous_dates.union_all(
        select(
            cte_portfolio_continuous_dates.c.portfolio_id,
            cte_portfolio_continuous_dates.c.checkpoint_date,
            func.date(cte_portfolio_continuous_dates.c.date, "+1 day").label("date"),
        ).where(cte_portfolio_continuous_dates.c.date < func.date("now"))
    )

    cte_1 = (
        select(
            PortfolioGroupPerformance.portfolio_id,
            PortfolioAggregate.checkpoint_date,
            PortfolioGroupPerformance.date,
            func.sum(PortfolioGroupPerformance.market_value).label("market_value"),
            func.sum(PortfolioGroupPerformance.market_value_adj).label(
                "market_value_adj"
            ),
            func.sum(PortfolioGroupPerformance.delta_quantity_value_adj).label(
                "delta_quantity_value_adj"
            ),
        )
        .join_from(
            PortfolioGroupPerformance,
            Portfolio,
            Portfolio.id == PortfolioGroupPerformance.portfolio_id,
        )
        .join(
            PortfolioAggregate,
            PortfolioAggregate.id == Portfolio.portfolio_aggregate_id,
        )
        .where(
            and_(
                PortfolioAggregate.user_id == user_id,
                PortfolioGroupPerformance.date >= PortfolioAggregate.checkpoint_date,
            )
        )
        .group_by(
            PortfolioGroupPerformance.portfolio_id,
            PortfolioGroupPerformance.date,
        )
    ).cte(name="cte_1")

    cte_2 = (
        select(
            cte_portfolio_continuous_dates.c.portfolio_id,
            cte_portfolio_continuous_dates.c.checkpoint_date,
            cte_portfolio_continuous_dates.c.date,
            func.coalesce(cte_1.c.market_value, 0.0).label("market_value"),
            func.coalesce(cte_1.c.market_value_adj, 0.0).label("market_value_adj"),
            func.coalesce(cte_1.c.delta_quantity_value_adj, 0.0).label(
                "delta_quantity_value_adj"
            ),
            func.coalesce(AdjustedPortfolioTransaction.cash_flow, 0.0).label(
                "cash_balance"
            ),
            func.coalesce(AdjustedPortfolioTransaction.invested_amount, 0.0).label(
                "invested_amount"
            ),
            func.coalesce(
                AdjustedPortfolioTransaction.invested_amount_total, 0.0
            ).label("invested_amount_total"),
            func.coalesce(
                AdjustedPortfolioTransaction.asset_disposal_income, 0.0
            ).label("asset_disposal_income"),
            func.coalesce(
                AdjustedPortfolioTransaction.asset_disposal_income_total, 0.0
            ).label("asset_disposal_income_total"),
            func.coalesce(AdjustedPortfolioTransaction.asset_holding_income, 0.0).label(
                "asset_holding_income"
            ),
            func.coalesce(
                AdjustedPortfolioTransaction.asset_holding_income_total, 0.0
            ).label("asset_holding_income_total"),
            func.coalesce(AdjustedPortfolioTransaction.interest_income, 0.0).label(
                "interest_income"
            ),
            func.coalesce(
                AdjustedPortfolioTransaction.interest_income_total, 0.0
            ).label("interest_income_total"),
            func.coalesce(AdjustedPortfolioTransaction.investment_income, 0.0).label(
                "investment_income"
            ),
            func.coalesce(
                AdjustedPortfolioTransaction.investment_income_total, 0.0
            ).label("investment_income_total"),
        )
        .outerjoin_from(
            cte_portfolio_continuous_dates,
            cte_1,
            and_(
                cte_1.c.portfolio_id == cte_portfolio_continuous_dates.c.portfolio_id,
                cte_1.c.date == cte_portfolio_continuous_dates.c.date,
            ),
        )
        .outerjoin(
            AdjustedPortfolioTransaction,
            and_(
                cte_portfolio_continuous_dates.c.portfolio_id
                == AdjustedPortfolioTransaction.portfolio_id,
                cte_portfolio_continuous_dates.c.date
                == AdjustedPortfolioTransaction.date,
            ),
        )
        .union_all(
            select(
                PortfolioPerformance.portfolio_id,
                PortfolioAggregate.checkpoint_date,
                PortfolioPerformance.date,
                PortfolioPerformance.market_value,
                PortfolioPerformance.market_value_adj,
                PortfolioPerformance.delta_quantity_value_adj,
                PortfolioPerformance.cash_balance,
                PortfolioPerformance.invested_amount,
                PortfolioPerformance.invested_amount_total,
                PortfolioPerformance.asset_disposal_income,
                PortfolioPerformance.asset_disposal_income_total,
                PortfolioPerformance.asset_holding_income,
                PortfolioPerformance.asset_holding_income_total,
                PortfolioPerformance.interest_income,
                PortfolioPerformance.interest_income_total,
                PortfolioPerformance.investment_income,
                PortfolioPerformance.investment_income_total,
            )
            .join_from(
                PortfolioPerformance,
                Portfolio,
                Portfolio.id == PortfolioPerformance.portfolio_id,
            )
            .join(
                PortfolioAggregate,
                PortfolioAggregate.id == Portfolio.portfolio_aggregate_id,
            )
            .where(
                and_(
                    PortfolioAggregate.user_id == user_id,
                    PortfolioPerformance.date
                    == func.date(PortfolioAggregate.checkpoint_date, "-1 day"),
                )
            )
        )
    ).cte(name="cte_2")

    cte_3 = (
        select(
            cte_2.c.portfolio_id,
            cte_2.c.checkpoint_date,
            cte_2.c.date,
            cte_2.c.market_value,
            cte_2.c.market_value_adj,
            cte_2.c.delta_quantity_value_adj,
            (
                func.sum(cte_2.c.cash_balance).over(
                    partition_by=cte_2.c.portfolio_id,
                    order_by=cte_2.c.date,
                )
            ).label("cash_balance"),
            (
                func.sum(cte_2.c.invested_amount).over(
                    partition_by=cte_2.c.portfolio_id,
                    order_by=cte_2.c.date,
                )
            ).label("invested_amount"),
            (
                func.sum(cte_2.c.invested_amount_total).over(
                    partition_by=cte_2.c.portfolio_id,
                    order_by=cte_2.c.date,
                )
            ).label("invested_amount_total"),
            func.sum(cte_2.c.asset_disposal_income)
            .over(
                partition_by=cte_2.c.portfolio_id,
                order_by=cte_2.c.date,
            )
            .label("asset_disposal_income"),
            func.sum(cte_2.c.asset_disposal_income_total)
            .over(
                partition_by=cte_2.c.portfolio_id,
                order_by=cte_2.c.date,
            )
            .label("asset_disposal_income_total"),
            func.sum(cte_2.c.asset_holding_income)
            .over(
                partition_by=cte_2.c.portfolio_id,
                order_by=cte_2.c.date,
            )
            .label("asset_holding_income"),
            func.sum(cte_2.c.asset_holding_income_total)
            .over(
                partition_by=cte_2.c.portfolio_id,
                order_by=cte_2.c.date,
            )
            .label("asset_holding_income_total"),
            func.sum(cte_2.c.interest_income)
            .over(
                partition_by=cte_2.c.portfolio_id,
                order_by=cte_2.c.date,
            )
            .label("interest_income"),
            func.sum(cte_2.c.interest_income_total)
            .over(
                partition_by=cte_2.c.portfolio_id,
                order_by=cte_2.c.date,
            )
            .label("interest_income_total"),
            (
                func.sum(cte_2.c.investment_income).over(
                    partition_by=cte_2.c.portfolio_id,
                    order_by=cte_2.c.date,
                )
            ).label("investment_income"),
            (
                func.sum(cte_2.c.investment_income_total).over(
                    partition_by=cte_2.c.portfolio_id,
                    order_by=cte_2.c.date,
                )
            ).label("investment_income_total"),
        )
        .distinct()
        .union_all(
            select(
                PortfolioPerformance.portfolio_id,
                PortfolioAggregate.checkpoint_date,
                PortfolioPerformance.date,
                PortfolioPerformance.market_value,
                PortfolioPerformance.market_value_adj,
                PortfolioPerformance.delta_quantity_value_adj,
                PortfolioPerformance.cash_balance,
                PortfolioPerformance.invested_amount,
                PortfolioPerformance.invested_amount_total,
                PortfolioPerformance.asset_disposal_income,
                PortfolioPerformance.asset_disposal_income_total,
                PortfolioPerformance.asset_holding_income,
                PortfolioPerformance.asset_holding_income_total,
                PortfolioPerformance.interest_income,
                PortfolioPerformance.interest_income_total,
                PortfolioPerformance.investment_income,
                PortfolioPerformance.investment_income_total,
            )
            .join_from(
                PortfolioPerformance,
                Portfolio,
                Portfolio.id == PortfolioPerformance.portfolio_id,
            )
            .join(
                PortfolioAggregate,
                PortfolioAggregate.id == Portfolio.portfolio_aggregate_id,
            )
            .where(
                and_(
                    PortfolioAggregate.user_id == user_id,
                    PortfolioPerformance.date
                    < func.date(PortfolioAggregate.checkpoint_date, "-1 day"),
                )
            )
        )
    ).cte(name="cte_3")

    cte_4 = select(
        cte_3,
        (
            cte_3.c.market_value + cte_3.c.invested_amount + cte_3.c.investment_income
        ).label("profit"),
        (
            cte_3.c.market_value
            + cte_3.c.invested_amount_total
            + cte_3.c.investment_income_total
        ).label("profit_total"),
        (
            (cte_3.c.market_value + cte_3.c.invested_amount + cte_3.c.investment_income)
            / func.abs(cte_3.c.invested_amount)
        ).label("profit_percentage"),
        (
            (
                cte_3.c.market_value
                + cte_3.c.invested_amount_total
                + cte_3.c.investment_income_total
            )
            / func.abs(cte_3.c.invested_amount_total)
        ).label("profit_percentage_total"),
        func.max(cte_3.c.market_value + cte_3.c.asset_disposal_income)
        .over(
            partition_by=cte_3.c.portfolio_id,
            order_by=cte_3.c.date,
        )
        .label("past_maximum_value"),
        func.max(cte_3.c.market_value + cte_3.c.asset_disposal_income_total)
        .over(
            partition_by=cte_3.c.portfolio_id,
            order_by=cte_3.c.date,
        )
        .label("past_maximum_value_total"),
        func.max(
            cte_3.c.market_value + cte_3.c.invested_amount + cte_3.c.investment_income
        )
        .over(
            partition_by=cte_3.c.portfolio_id,
            order_by=cte_3.c.date,
        )
        .label("past_maximum_profit"),
        func.max(
            cte_3.c.market_value
            + cte_3.c.invested_amount_total
            + cte_3.c.investment_income_total
        )
        .over(
            partition_by=cte_3.c.portfolio_id,
            order_by=cte_3.c.date,
        )
        .label("past_maximum_profit_total"),
        func.coalesce(
            (
                (cte_3.c.market_value_adj - cte_3.c.delta_quantity_value_adj)
                / func.lag(cte_3.c.market_value_adj).over(
                    partition_by=cte_3.c.portfolio_id,
                    order_by=cte_3.c.date,
                )
                - 1
            ),
            0.0,
        ).label("hpr"),
        (
            func.row_number().over(
                partition_by=cte_3.c.portfolio_id,
                order_by=cte_3.c.date,
            )
        ).label("row_number"),
        (
            cte_3.c.invested_amount
            - func.lag(cte_3.c.invested_amount, 1, 0.0).over(
                partition_by=cte_3.c.portfolio_id,
                order_by=cte_3.c.date,
            )
            + cte_3.c.investment_income
            - func.lag(cte_3.c.investment_income, 1, 0.0).over(
                partition_by=cte_3.c.portfolio_id,
                order_by=cte_3.c.date,
            )
        ).label("cash_flow"),
        (
            cte_3.c.invested_amount_total
            - func.lag(cte_3.c.invested_amount_total, 1, 0.0).over(
                partition_by=cte_3.c.portfolio_id,
                order_by=cte_3.c.date,
            )
            + cte_3.c.investment_income_total
            - func.lag(cte_3.c.investment_income_total, 1, 0.0).over(
                partition_by=cte_3.c.portfolio_id,
                order_by=cte_3.c.date,
            )
        ).label("cash_flow_total"),
    ).cte(name="cte_4")

    cte_5 = select(
        cte_4,
        (
            func.exp(
                func.sum(func.ln(1 + cte_4.c.hpr)).over(
                    partition_by=cte_4.c.portfolio_id,
                    order_by=cte_4.c.date,
                )
            )
        ).label("hpr_cumulative"),
        (cte_4.c.row_number / 365.0).label("years_passed"),
        func.nullif(cte_4.c.hpr, 0.0).label("hpr_non_zero"),
        (
            func.xirr(
                cte_4.c.date,
                cte_4.c.cash_flow,
                cte_4.c.market_value,
                cte_4.c.checkpoint_date,
            ).over(
                partition_by=cte_4.c.portfolio_id,
                order_by=cte_4.c.date,
            )
        ).label("xirr_rate"),
        (
            func.xirr(
                cte_4.c.date,
                cte_4.c.cash_flow_total,
                cte_4.c.market_value,
                cte_4.c.checkpoint_date,
            ).over(
                partition_by=cte_4.c.portfolio_id,
                order_by=cte_4.c.date,
            )
        ).label("xirr_rate_total"),
    ).cte(name="cte_5")

    cte_6 = select(
        cte_5,
        (
            func.max(cte_5.c.hpr_cumulative).over(
                partition_by=cte_5.c.portfolio_id,
                order_by=cte_5.c.date,
            )
        ).label("past_maximum_hpr_cumulative"),
        (
            func.avg(cte_5.c.hpr_non_zero).over(
                partition_by=cte_5.c.portfolio_id,
                order_by=cte_5.c.date,
            )
        ).label("hpr_non_zero_avg"),
        (
            func.stddev(cte_5.c.hpr_non_zero).over(
                partition_by=cte_5.c.portfolio_id,
                order_by=cte_5.c.date,
            )
        ).label("hpr_non_zero_stddev"),
        (
            func.stddev(
                func.iif(cte_5.c.hpr_non_zero < 0, cte_5.c.hpr_non_zero, None)
            ).over(
                partition_by=cte_5.c.portfolio_id,
                order_by=cte_5.c.date,
            )
        ).label("hpr_non_zero_stddev_d"),
        (
            func.count(cte_5.c.hpr_non_zero).over(
                partition_by=cte_5.c.portfolio_id,
                order_by=cte_5.c.date,
            )
            * 365.0
            / cte_5.c.row_number
        ).label("avg_days_per_year"),
    ).cte(name="cte_6")

    query = select(
        cte_6.c.portfolio_id,
        cte_6.c.date,
        cte_6.c.market_value,
        cte_6.c.market_value_adj,
        cte_6.c.delta_quantity_value_adj,
        cte_6.c.cash_balance,
        cte_6.c.invested_amount,
        cte_6.c.invested_amount_total,
        cte_6.c.asset_disposal_income,
        cte_6.c.asset_disposal_income_total,
        cte_6.c.asset_holding_income,
        cte_6.c.asset_holding_income_total,
        cte_6.c.interest_income,
        cte_6.c.interest_income_total,
        cte_6.c.investment_income,
        cte_6.c.investment_income_total,
        cte_6.c.profit,
        cte_6.c.profit_total,
        func.coalesce(cte_6.c.profit_percentage, 0.0).label("profit_percentage"),
        func.coalesce(cte_6.c.profit_percentage_total, 0.0).label(
            "profit_percentage_total"
        ),
        func.coalesce(
            (cte_6.c.market_value + cte_6.c.asset_disposal_income)
            / cte_6.c.past_maximum_value
            - 1,
            0.0,
        ).label("drawdown_value"),
        func.coalesce(
            (cte_6.c.market_value + cte_6.c.asset_disposal_income_total)
            / cte_6.c.past_maximum_value_total
            - 1,
            0.0,
        ).label("drawdown_value_total"),
        func.coalesce(
            (cte_6.c.profit - cte_6.c.past_maximum_profit) / cte_6.c.past_maximum_value,
            0.0,
        ).label("drawdown_profit"),
        func.coalesce(
            (cte_6.c.profit_total - cte_6.c.past_maximum_profit_total)
            / cte_6.c.past_maximum_value_total,
            0.0,
        ).label("drawdown_profit_total"),
        cte_6.c.hpr,
        (cte_6.c.hpr_cumulative / cte_6.c.past_maximum_hpr_cumulative - 1).label(
            "drawdown"
        ),
        (cte_6.c.hpr_cumulative - 1).label("twrr_rate_daily"),
        (func.pow(cte_6.c.hpr_cumulative, 1.0 / cte_6.c.years_passed) - 1).label(
            "twrr_rate_annualized"
        ),
        (cte_6.c.hpr_non_zero_avg / cte_6.c.hpr_non_zero_stddev).label(
            "sharpe_ratio_daily"
        ),
        (
            cte_6.c.hpr_non_zero_avg
            / cte_6.c.hpr_non_zero_stddev
            * func.pow(cte_6.c.avg_days_per_year, 0.5)
        ).label("sharpe_ratio_annualized"),
        (cte_6.c.hpr_non_zero_avg / cte_6.c.hpr_non_zero_stddev_d).label(
            "sortino_ratio_daily"
        ),
        (
            cte_6.c.hpr_non_zero_avg
            / cte_6.c.hpr_non_zero_stddev_d
            * func.pow(cte_6.c.avg_days_per_year, 0.5)
        ).label("sortino_ratio_annualized"),
        cte_6.c.xirr_rate,
        cte_6.c.xirr_rate_total,
    ).where(cte_6.c.date >= cte_6.c.checkpoint_date)

    return insert(PortfolioPerformance).from_select(
        [
            "portfolio_id",
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
