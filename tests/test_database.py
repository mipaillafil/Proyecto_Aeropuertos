from api.database import obtener_datos, obtener_estadisticas


def test_obtener_datos():
    df = obtener_datos(limit=10)

    assert df is not None
    assert len(df) > 0
    assert "cnt_operaciones" in df.columns


def test_obtener_estadisticas():
    stats = obtener_estadisticas()

    assert "total_registros" in stats
    assert "promedio_operaciones" in stats
    assert stats["total_registros"] > 0